import "../styles/home.css";

function Home() {
  return (
    <div className="home">

      <section className="hero">

        <div className="live-status">
          <span className="live-dot"></span>
          <span>LIVE MONITORING ACROSS Tehri</span>
        </div>

        <h1>
          Predict landslide risk <span> before </span> it becomes a disaster.
        </h1>

        <p>
          PahadSuraksha combines rainfall telemetry, terrain slope, soil saturation, and historical incident data to give Drivers and district authorities an early, explainable warning across Tehri.
        </p>

        <div className="hero-buttons">
          <button className="primary-btn">
            Check risk
          </button>

          <button className="secondary-btn">
            learn more
          </button>
        </div>

      </section>

    </div>
  );
}

export default Home;