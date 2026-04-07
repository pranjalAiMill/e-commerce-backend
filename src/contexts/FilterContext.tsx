import { createContext, useContext, useState, ReactNode } from 'react';

interface FilterContextType {
  selectedChannels: Set<string>;
  setSelectedChannels: (channels: Set<string>) => void;
  toggleChannel: (channel: string) => void;
  getSelectedMarketplaces: () => string[];
  selectedRegion: string;
  setSelectedRegion: (region: string) => void;
}

const FilterContext = createContext<FilterContextType | undefined>(undefined);

// Map frontend channel names to backend marketplace names
const CHANNEL_TO_MARKETPLACE: Record<string, string[]> = {
  "Amazon": ["Amazon.in", "Amazon.com"],
  "Flipkart": ["Flipkart"],
  "Takealot": ["Takealot"],
  "Shopify": ["Shopify"],
  "eBay": ["eBay"],
  "Magento": ["Magento"],
  "WooCommerce": ["WooCommerce"],
  "Myntra": ["Myntra"],
  "Walmart": ["Walmart"],
  "Checkers": ["Checkers"],
  "Woolworths": ["Woolworths"],
  "Makro": ["Makro"],
};

const ALL_CHANNELS = Object.keys(CHANNEL_TO_MARKETPLACE);

export function FilterProvider({ children }: { children: ReactNode }) {
  const [selectedChannels, setSelectedChannels] = useState<Set<string>>(
    new Set(ALL_CHANNELS)
  );
  const [selectedRegion, setSelectedRegion] = useState<string>("global");

  const toggleChannel = (channel: string) => {
    const newChannels = new Set(selectedChannels);
    if (newChannels.has(channel)) {
      newChannels.delete(channel);
    } else {
      newChannels.add(channel);
    }
    setSelectedChannels(newChannels);
  };

  const getSelectedMarketplaces = (): string[] => {
    const marketplaces: string[] = [];
    selectedChannels.forEach((channel) => {
      const mapped = CHANNEL_TO_MARKETPLACE[channel];
      if (mapped) {
        marketplaces.push(...mapped);
      }
    });
    return marketplaces;
  };

  return (
    <FilterContext.Provider
      value={{
        selectedChannels,
        setSelectedChannels,
        toggleChannel,
        getSelectedMarketplaces,
        selectedRegion,
        setSelectedRegion,
      }}
    >
      {children}
    </FilterContext.Provider>
  );
}

export function useFilters() {
  const context = useContext(FilterContext);
  if (!context) {
    throw new Error('useFilters must be used within a FilterProvider');
  }
  return context;
}
