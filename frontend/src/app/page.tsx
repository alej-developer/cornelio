export default function Home() {
  return (
    <main className="container">
      <header className="header">
        <h1>Cornelio</h1>
        <p className="subtitle">MLX Inference Platform</p>
      </header>

      <section className="status-card">
        <div className="status-indicator" />
        <div>
          <h2>System Status</h2>
          <p>Backend connection pending configuration.</p>
        </div>
      </section>

      <footer className="footer">
        <p>Cornelio v0.1.0 — Powered by Apple MLX</p>
      </footer>
    </main>
  );
}
