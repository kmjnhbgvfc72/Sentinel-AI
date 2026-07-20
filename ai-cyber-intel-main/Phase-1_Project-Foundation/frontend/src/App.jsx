import Header from "./components/Header";
import Dashboard from "./pages/Dashboard";

export default function App() {
  return (
    <div className="app-shell">
      <Header />
      <main className="main-content">
        <Dashboard />
      </main>
    </div>
  );
}
