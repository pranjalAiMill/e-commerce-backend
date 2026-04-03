# from typing import Literal

# from langchain_openai import ChatOpenAI
# from langchain_core.output_parsers import StrOutputParser
# from langchain_core.prompts import ChatPromptTemplate


# Verdict = Literal["Match", "Mismatch"]


# class ColorMatchAgent:
#     """
#     LangChain-based agent that decides if a detected color matches
#     the catalog color.

#     This uses an OpenAI model via LangChain and applies catalog rules such as:
#     - "sky blue" is a shade of "blue" -> Match
#     - "navy" vs. "blue" -> Match
#     - "cream" vs. "white" -> Match
#     - "red" vs. "green" -> Mismatch
#     """

#     def __init__(self, openai_api_key: str, model_name: str = "gpt-4o-mini") -> None:
#         """
#         Initialize the agent.

#         Parameters
#         ----------
#         openai_api_key : str
#             OpenAI API key.
#         model_name : str
#             Name of OpenAI chat model to use.
#         """
#         # ChatOpenAI will also read OPENAI_API_KEY from environment,
#         # but we pass it explicitly for clarity.
#         self.llm = ChatOpenAI(
#             model=model_name,
#             temperature=0,
#             openai_api_key=openai_api_key,
#         )
#         self._chain = self._build_chain()

#     def _build_chain(self):
#         """Build the LangChain pipeline that returns "Match" or "Mismatch"""
#         template = ChatPromptTemplate.from_template(
#             """
# You are an ecommerce color matching expert.

# Catalog (expected) color: "{expected_color}"
# Detected color from image model: "{detected_color}"

# Decide whether a typical shopper would consider these the SAME color
# (for example, "sky blue" is a shade of "blue", "navy" is also "blue",
# "off white" is "white", "navy blue" is "dark blue", etc.).

# Respond with exactly ONE word:
# - "Match"  if they are similar color or shade.
# - "Mismatch" if they are different.

# Do not add any explanation or punctuation. Just return Match or Mismatch.
#             """.strip()
#         )
#         parser = StrOutputParser()
#         return template | self.llm | parser

#     def get_verdict(self, expected_color: str, detected_color: str) -> Verdict:
#         """
#         Determine whether the detected color matches the expected catalog color.

#         Parameters
#         ----------
#         expected_color : str
#             Color from the dataset.
#         detected_color : str
#             Color predicted by CLIP.

#         Returns
#         -------
#         Verdict
#             "Match" or "Mismatch".
#         """
#         raw = self._chain.invoke(
#             {
#                 "expected_color": expected_color.strip(),
#                 "detected_color": detected_color.strip(),
#             }
#         )
#         # Normalize to exactly "Match" or "Mismatch".
#         normalized = raw.strip().lower()
#         if "match" in normalized and "mis" not in normalized:
#             return "Match"
#         if "mismatch" in normalized:
#             return "Mismatch"
#         # Fallback: be conservative and mark as mismatch
#         return "Mismatch"



from typing import Literal, TypedDict
from langchain_openai import ChatOpenAI
import json

Verdict = Literal["Match", "Mismatch"]


class VerdictResult(TypedDict):
    verdict: Verdict
    confidence: float
    reason: str


class ColorMatchAgent:
    """
    LangChain-based agent that decides if a detected color matches
    the catalog color, and returns an LLM-generated confidence score.
    """

    def __init__(self, openai_api_key: str, model_name: str = "gpt-4o-mini") -> None:
        self.llm = ChatOpenAI(
            model=model_name,
            temperature=0,
            openai_api_key=openai_api_key,
            max_tokens=150,
        )

    def get_verdict(self, expected_color: str, detected_color: str) -> Verdict:
        """
        Returns "Match" or "Mismatch". Backward-compatible with existing pipeline.
        """
        result = self.get_verdict_with_confidence(expected_color, detected_color)
        return result["verdict"]

    def get_verdict_with_confidence(
        self, expected_color: str, detected_color: str
    ) -> VerdictResult:
        """
        Returns verdict, LLM-generated confidence score, and reasoning.
        """
        # Normalize inputs to avoid trivial mismatches from whitespace
        expected_color = expected_color.strip().lower()
        detected_color = detected_color.strip().lower()

        # Fast path: exact match — no LLM call needed
        if expected_color == detected_color:
            return VerdictResult(
                verdict="Match",
                confidence=1.0,
                reason="Exact color match.",
            )

        prompt = f"""
You are a color matching expert for an ecommerce fashion platform.

Catalog color (expected): "{expected_color}"
Detected color (from image): "{detected_color}"

Decide whether these two colors belong to the same color family.
Use your general knowledge of colors — consider shades, tints, tones,
and common color variants. If a typical online shopper would consider
them the same color or a close variant, it is a Match.

Respond ONLY with valid JSON, no markdown.

{{
    "verdict": "Match" or "Mismatch",
    "confidence": <float between 0.0 and 1.0>,
    "reason": "<one short sentence>"
}}
        """.strip()

        try:
            raw = self.llm.invoke([("user", prompt)]).content.strip()

            if raw.startswith("```json"):
                raw = raw.replace("```json", "").replace("```", "").strip()
            elif raw.startswith("```"):
                raw = raw.replace("```", "").strip()

            parsed = json.loads(raw)

            raw_verdict = str(parsed.get("verdict", "")).strip().lower()
            verdict: Verdict = (
                "Match"
                if "match" in raw_verdict and "mis" not in raw_verdict
                else "Mismatch"
            )

            return VerdictResult(
                verdict=verdict,
                confidence=float(parsed.get("confidence", 0.0)),
                reason=parsed.get("reason", ""),
            )

        except Exception as e:
            print(f"ColorMatchAgent error: {e}")
            return VerdictResult(verdict="Mismatch", confidence=0.0, reason=str(e))