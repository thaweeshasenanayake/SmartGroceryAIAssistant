import { Check, Lightbulb } from "lucide-react";
import type { HealthResponse } from "../Interfaces";

interface Props {
  suggestion: HealthResponse;
  onAccept: () => void;
  onIgnore: () => void;
}

export default function HealthModal({ suggestion, onAccept, onIgnore }: Props) {
  return (
    <div className="modal-overlay">
      <div className="modal">
        <div className="modal-header">
          <Lightbulb className="icon-yellow" />
          <h3>Healthier Choice Detected!</h3>
        </div>
        <p>{suggestion.message}</p>
        <div className="modal-actions">
          <button onClick={onAccept} className="btn-green">
            <Check size={16} /> Yes, switch to {suggestion.alternative}
          </button>
          <button onClick={onIgnore} className="btn-gray">
            No, keep {suggestion.original.name}
          </button>
        </div>
      </div>
    </div>
  );
}
