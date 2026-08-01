import "../styles/footer.css";

function Footer() {
  return (
    <footer className="footer">

      <div className="footer-container">

        <div className="footer-section">
          <h2 className="footer-logo">
            <span className="pahad">Pahad</span>
            <span className="suraksha">Suraksha</span>
          </h2>

          <p className="footer-description">
            AI-powered platform for safer travel and landslide awareness in Uttarakhand.
          </p>
        </div>

        <div className="footer-section">
          <h3>Emergency Contacts</h3>

          <p>
             Disaster Management: <strong>1070</strong>
          </p>

          <p>
            Emergency Helpline: <strong>112</strong>
          </p>

          <p>
            National Highway Helpline: <strong>1033</strong>
          </p>

        </div>

      </div>

      <div className="footer-bottom">

        <p>
          © {new Date().getFullYear()} PAHADSURAKSHA. All Rights Reserved.
        </p>

        <p>
          Designed & Developed for Safer Roads in Uttarakhand.
        </p>

      </div>

    </footer>
  );
}

export default Footer;