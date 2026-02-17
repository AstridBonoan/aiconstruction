export function Card({ children, className = '' }) {
  return (
    <div
      className={`rounded-xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 shadow-sm ${className}`}
    >
      {children}
    </div>
  );
}

export function CardHeader({ title, subtitle }) {
  return (
    <div className="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
      <h3 className="text-lg font-semibold text-gray-900 dark:text-white">{title}</h3>
      {subtitle && <p className="text-sm text-gray-500 dark:text-gray-400 mt-0.5">{subtitle}</p>}
    </div>
  );
}

export function CardBody({ children, className = '' }) {
  return <div className={`px-6 py-4 ${className}`}>{children}</div>;
}
