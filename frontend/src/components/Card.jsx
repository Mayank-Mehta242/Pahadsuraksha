export default function Card({ children, className = "", title, action }) {
  return (
    <div className={`card ${className}`}>
      {(title || action) && (
        <div className="flex items-start justify-between gap-3 mb-4">
          <div>
            {title && <h3 className="text-lg sm:text-xl font-semibold text-white">{title}</h3>}
          </div>
          {action}
        </div>
      )}
      {children}
    </div>
  );
}
