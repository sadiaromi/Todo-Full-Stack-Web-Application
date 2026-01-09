import React from "react";

const TaskFilter = ({ currentFilter, setFilter }) => {
  const filters = ["All", "Completed", "Pending"];

  return (
    <div className="flex gap-3 mb-4 justify-center">
      {filters.map((filter) => (
        <button
          key={filter}
          onClick={() => setFilter(filter)}
          className={`px-3 py-1 rounded-md ${
            currentFilter === filter
              ? "bg-pink-500 text-white"
              : "bg-pink-100 text-pink-700 hover:bg-pink-200"
          } transition`}
        >
          {filter}
        </button>
      ))}
    </div>
  );
};

export default TaskFilter;
