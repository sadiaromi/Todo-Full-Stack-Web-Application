// Performance optimization utilities for the Todo App

/**
 * Memoization utility to cache function results
 * @param {Function} fn - Function to memoize
 * @returns {Function} - Memoized function
 */
export function memoize(fn) {
  const cache = new Map();
  return function (...args) {
    const key = JSON.stringify(args);
    if (cache.has(key)) {
      return cache.get(key);
    }
    const result = fn.apply(this, args);
    cache.set(key, result);
    return result;
  };
}

/**
 * Debounce utility to delay function execution
 * @param {Function} func - Function to debounce
 * @param {number} delay - Delay in milliseconds
 * @returns {Function} - Debounced function
 */
export function debounce(func, delay) {
  let timeoutId;
  return function (...args) {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => func.apply(this, args), delay);
  };
}

/**
 * Throttle utility to limit function execution frequency
 * @param {Function} func - Function to throttle
 * @param {number} limit - Time limit in milliseconds
 * @returns {Function} - Throttled function
 */
export function throttle(func, limit) {
  let inThrottle;
  return function (...args) {
    if (!inThrottle) {
      func.apply(this, args);
      inThrottle = true;
      setTimeout(() => inThrottle = false, limit);
    }
  };
}

/**
 * Lazy loading utility for images
 * @param {string} src - Image source
 * @param {Object} options - Intersection observer options
 * @returns {Promise} - Promise that resolves when image loads
 */
export function lazyLoadImage(src, options = {}) {
  return new Promise((resolve, reject) => {
    const img = new Image();
    img.onload = () => resolve(img);
    img.onerror = reject;
    img.src = src;
  });
}

/**
 * Virtual scrolling helper to render only visible items
 * @param {Array} items - Array of items to render
 * @param {number} startIndex - Start index of visible items
 * @param {number} endIndex - End index of visible items
 * @returns {Array} - Visible items
 */
export function virtualScroll(items, startIndex, endIndex) {
  return items.slice(startIndex, endIndex + 1);
}

/**
 * Efficient array filtering with early termination
 * @param {Array} array - Array to filter
 * @param {Function} predicate - Filter function
 * @param {number} maxResults - Maximum results to return (optional)
 * @returns {Array} - Filtered results
 */
export function efficientFilter(array, predicate, maxResults = null) {
  if (maxResults === null) {
    return array.filter(predicate);
  }

  const result = [];
  for (let i = 0; i < array.length; i++) {
    if (predicate(array[i])) {
      result.push(array[i]);
      if (result.length >= maxResults) {
        break;
      }
    }
  }
  return result;
}

/**
 * Batch updates to reduce re-renders
 * @param {Function} updateFn - Function to batch
 * @returns {Function} - Batched function
 */
export function batchUpdates(updateFn) {
  let scheduled = false;
  let updates = [];

  return function (...args) {
    updates.push({ fn: updateFn, args });

    if (!scheduled) {
      scheduled = true;
      Promise.resolve().then(() => {
        const batchedUpdates = [...updates];
        updates = [];
        scheduled = false;

        batchedUpdates.forEach(({ fn, args }) => {
          fn(...args);
        });
      });
    }
  };
}

/**
 * Optimize rendering with requestAnimationFrame
 * @param {Function} callback - Callback to execute
 * @returns {number} - Animation frame ID
 */
export function optimizedRender(callback) {
  return requestAnimationFrame(callback);
}

/**
 * Cleanup function for performance utilities
 */
export function cleanup() {
  // Clear caches, cancel animation frames, etc.
  // This would be called when components unmount
}