import { AlertTriangle } from "lucide-react";
import type { Alert } from "../Interfaces";

interface Props {
  alerts: Alert[];
}

export default function AlertsCard({ alerts }: Props) {
  return (
    <div className="card">
      <h2>
        <AlertTriangle size={20} /> Expiry Alerts
      </h2>

      {alerts.length === 0 && <p className="empty">Everything is fresh!</p>}

      <ul className="list">
        {alerts.map((a, idx) => (
          <li key={idx} className={`list-item alert ${a.status.toLowerCase()}`}>
            <strong>{a.item}</strong>
            <span>{a.days_left} days left</span>
          </li>
        ))}
      </ul>
    </div>
  );
}
