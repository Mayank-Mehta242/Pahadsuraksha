export default function Card({ children, className = "", title, action }) {
  return (
    <div className={`card ${className}`}>
      {(title || action) && (
        <div className="flex items-start justify-between mb-4">
          <div>
            {title && <h3 className="text-lg font-semibold text-white">{title}</h3>}
          </div>
          {action}
        </div>
      )}
      {children}
    </div>
  );
}
