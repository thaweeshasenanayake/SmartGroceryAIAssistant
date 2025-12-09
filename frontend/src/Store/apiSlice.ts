import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";
import type { InventoryItem, Prediction, Alert, HealthResponse } from "../Interfaces";

export const api = createApi({
  reducerPath: "api",
  baseQuery: fetchBaseQuery({ baseUrl: "/api" }), // Proxy handles the rest
  tagTypes: ["Inventory", "Predictions", "Alerts"], // Used for auto-refreshing
  endpoints: (builder) => ({
    // --- QUERIES (Get Data) ---
    getInventory: builder.query<InventoryItem[], void>({
      query: () => "/inventory",
      providesTags: ["Inventory"],
    }),
    getPredictions: builder.query<{ predictions: Prediction[] }, void>({
      query: () => "/predictions",
      providesTags: ["Predictions"],
    }),
    getAlerts: builder.query<{ alerts: Alert[] }, void>({
      query: () => "/alerts",
      providesTags: ["Alerts"],
    }),

    // --- MUTATIONS (Change Data) ---
    addItem: builder.mutation<HealthResponse | { status: string; message: string }, InventoryItem>({
      query: (newItem) => ({
        url: "/add-item",
        method: "POST",
        body: newItem,
      }),
      // Invalidates Inventory ONLY if it wasn't a suggestion (optional advanced logic),
      // but simpler: Just add invalidatesTags: ['Inventory'] here too.
      // It won't hurt if we re-fetch during a suggestion.
      invalidatesTags: ["Inventory"],
    }),

    forceAddItem: builder.mutation<{ status: string }, InventoryItem>({
      query: (item) => ({
        url: "/force-add-item",
        method: "POST",
        body: item,
      }),
      // When this succeeds, force re-fetch of all lists
      invalidatesTags: ["Inventory", "Predictions", "Alerts"],
    }),
  }),
});

// Export hooks for usage in functional components
export const {
  useGetInventoryQuery,
  useGetPredictionsQuery,
  useGetAlertsQuery,
  useAddItemMutation,
  useForceAddItemMutation,
} = api;
