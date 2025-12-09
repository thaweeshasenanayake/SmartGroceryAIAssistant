// --- Types & Interfaces ---

export interface InventoryItem {
  name: string;
  category: string;
  shelf_life_days: number;
  last_bought?: string; // Optional because backend fills it if missing
}

export interface Prediction {
  item: string;
  reason: string;
}

export interface Alert {
  item: string;
  days_left: number;
  status: string;
}

export interface HealthResponse {
  status: string;
  message: string;
  alternative: string;
  original: InventoryItem;
}