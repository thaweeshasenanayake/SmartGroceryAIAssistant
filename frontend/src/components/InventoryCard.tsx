import type { FormEvent, ChangeEvent } from "react";
import { Plus, ShoppingCart } from "lucide-react";
import type { InventoryItem } from "../Interfaces";

interface Props {
  inventory: InventoryItem[];
  newItem: InventoryItem;
  onInputChange: (e: ChangeEvent<HTMLInputElement>) => void;
  onAddItem: (e: FormEvent) => void;
}

export default function InventoryCard({ inventory, newItem, onInputChange, onAddItem }: Props) {
  return (
    <div className="card">
      <h2>
        <ShoppingCart size={20} /> Inventory
      </h2>

      <form onSubmit={onAddItem} className="add-form">
        <input type="text" placeholder="Item Name (e.g. Soda)" value={newItem.name} onChange={onInputChange} required />
        <button type="submit">
          <Plus size={20} />
        </button>
      </form>

      <ul className="list">
        {inventory.map((item, idx) => (
          <li key={idx} className="list-item">
            <span>{item.name}</span>
            <span className="tag">{item.category}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}
