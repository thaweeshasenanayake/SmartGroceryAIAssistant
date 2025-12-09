import { useState, type FormEvent, type ChangeEvent } from "react";
import "./App.css";
import type { InventoryItem, HealthResponse } from "./Interfaces";

// Import RTK Query Hooks (Auto-fetch & Cache)
import {
  useGetInventoryQuery,
  useGetPredictionsQuery,
  useGetAlertsQuery,
  useAddItemMutation,
  useForceAddItemMutation,
} from "./Store/apiSlice";

// Import Components
import HealthModal from "./components/HealthModal";
import InventoryCard from "./components/InventoryCard";
import PredictionsCard from "./components/PredictionsCard";
import AlertsCard from "./components/AlertsCard";

function App() {
  // --- LOCAL STATE (Only for UI interactions) ---
  const [newItem, setNewItem] = useState<InventoryItem>({
    name: "",
    shelf_life_days: 7,
    category: "General",
  });

  // Controls the "Healthier Choice" popup
  const [healthSuggestion, setHealthSuggestion] = useState<HealthResponse | null>(null);

  // --- RTK QUERY HOOKS ---
  // These automatically fetch data on mount and keep it fresh
  const { data: inventory = [] } = useGetInventoryQuery();
  const { data: predData } = useGetPredictionsQuery();
  const { data: alertData } = useGetAlertsQuery();

  const [addItem] = useAddItemMutation();
  const [forceAddItem] = useForceAddItemMutation();

  // Helper variables to safely access nested data
  const predictions = predData?.predictions || [];
  const alerts = alertData?.alerts || [];

  // --- HANDLERS ---

  // 1. Handle "Add" Button Click
  const handleAddItem = async (e: FormEvent) => {
    e.preventDefault();
    if (!newItem.name) return;

    try {
      // We use .unwrap() to get the raw response data or catch errors
      const response = await addItem(newItem).unwrap();

      if ("status" in response && response.status === "suggestion") {
        // AI found a healthier alternative -> Show Modal
        setHealthSuggestion(response as HealthResponse);
      } else {
        // Success -> Clear form (RTK automatically updates the list)
        setNewItem({ ...newItem, name: "" });
      }
    } catch (error) {
      console.error("Failed to add item:", error);
    }
  };

  // 2. Handle Modal Decision (Accept or Ignore)
  const handleDecision = async (overrideItem?: InventoryItem) => {
    try {
      // If overrideItem exists (User clicked Yes), use it. Otherwise use original (User clicked No).
      const itemToSend = overrideItem || newItem;

      // Force add bypasses the health check
      await forceAddItem(itemToSend).unwrap();

      // Reset UI
      setHealthSuggestion(null);
      setNewItem({ ...newItem, name: "" });
    } catch (error) {
      console.error("Failed to force add item:", error);
    }
  };

  // --- RENDER ---
  return (
    <div className="container">
      <header>
        <h1>🛒 Smart Grocery AI Assistant</h1>
      </header>

      {/* Popup Modal for Health Suggestions */}
      {healthSuggestion && (
        <HealthModal
          suggestion={healthSuggestion}
          onAccept={() => handleDecision({ ...newItem, name: healthSuggestion.alternative })}
          onIgnore={() => handleDecision()}
        />
      )}

      {/* Main Dashboard Layout */}
      <div className="main-layout">
        {/* LEFT COLUMN: Main Interaction (Wider) */}
        <div className="main-content">
          <InventoryCard
            inventory={inventory}
            newItem={newItem}
            onInputChange={(e: ChangeEvent<HTMLInputElement>) => setNewItem({ ...newItem, name: e.target.value })}
            onAddItem={handleAddItem}
          />
        </div>

        {/* RIGHT COLUMN: AI Insights (Narrower Sidebar) */}
        <div className="sidebar">
          <PredictionsCard predictions={predictions} />
          <AlertsCard alerts={alerts} />
        </div>
      </div>
    </div>
  );
}

export default App;
