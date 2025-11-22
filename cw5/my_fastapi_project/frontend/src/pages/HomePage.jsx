import { useMemo, useState } from "react";
import ItemList from "../components/ItemList.jsx";
import useItems from "../hooks/useItems.js";
import api from "../services/api.js";

const titles = ["Практика", "Экспресс", "Идея", "Концепт", "Драфт"];
const descriptions = [
  "Создано через демонстрационную кнопку.",
  "Тестовый элемент для проверки CRUD.",
  "Можно удалить или обновить через API.",
];

function randomChoice(list) {
  return list[Math.floor(Math.random() * list.length)];
}

function HomePage() {
  const { items, loading, error, refetch } = useItems();
  const [panelMessage, setPanelMessage] = useState("Нажмите кнопку, чтобы создать демо-товар.");
  const [creating, setCreating] = useState(false);

  const totalPrice = useMemo(() => items.reduce((sum, item) => sum + (item.price ?? 0), 0), [items]);

  const handleCreateDemo = () => {
    if (creating) return;
    setCreating(true);
    setPanelMessage("Создаём демо-товар...");

    const payload = {
      title: `${randomChoice(titles)} #${String(Date.now()).slice(-4)}`,
      description: randomChoice(descriptions),
      price: Math.floor(Math.random() * 900) + 100,
    };

    api
      .post("/items", payload)
      .then((response) => {
        setPanelMessage(`Создано: ${response.data.title}`);
        refetch();
      })
      .catch((err) => {
        setPanelMessage(`Не удалось создать товар: ${err.message}`);
      })
      .finally(() => setCreating(false));
  };

  return (
    <section className="panel">
      <div className="panel-header">
        <div>
          <h2>Добро пожаловать!</h2>
          <p>
            Этот экран доказывает, что связка FastAPI + React живая: ниже можно добавить демо-товар и
            увидеть его в списке.
          </p>
        </div>
        <div className="stats">
          <div>
            <span className="stats-label">Товаров</span>
            <strong className="stats-value">{items.length}</strong>
          </div>
          <div>
            <span className="stats-label">Сумма, ₽</span>
            <strong className="stats-value">{totalPrice}</strong>
          </div>
        </div>
      </div>

      <div className="panel-controls">
        <button className="primary-btn" onClick={handleCreateDemo} disabled={creating}>
          {creating ? "Создаём..." : "Создать демо-товар"}
        </button>
        <span className="panel-message">{panelMessage}</span>
      </div>

      <ItemList items={items} loading={loading} error={error} />
    </section>
  );
}

export default HomePage;
