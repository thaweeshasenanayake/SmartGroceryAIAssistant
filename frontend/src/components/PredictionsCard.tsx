import { Lightbulb } from "lucide-react";
import type { Prediction } from "../Interfaces";

interface Props {
  predictions: Prediction[];
}

export default function PredictionsCard({ predictions }: Props) {
  return (
    <div className="card">
      <h2>
        <Lightbulb size={20} /> Smart Predictions
      </h2>
      <p className="subtext">Based on your buying habits</p>

      {predictions.length === 0 && <p className="empty">No predictions yet.</p>}

      <ul className="list">
        {predictions.map((p, idx) => (
          <li key={idx} className="list-item prediction">
            <strong>{p.item}</strong>
            <small>{p.reason}</small>
          </li>
        ))}
      </ul>
    </div>
  );
}
