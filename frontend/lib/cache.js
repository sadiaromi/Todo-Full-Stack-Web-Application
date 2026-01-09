// Caching utilities for the Todo App

class Cache {
  constructor(options = {}) {
    this.cache = new Map();
    this.maxSize = options.maxSize || 100;
    this.ttl = options.ttl || 5 * 60 * 1000; // 5 minutes default
    this.cleanupInterval = options.cleanupInterval || 60 * 1000; // 1 minute

    // Start periodic cleanup
    this.startCleanup();
  }

  /**
   * Set a value in the cache
   * @param {string} key - Cache key
   * @param {*} value - Value to cache
   * @param {number} ttl - Time to live in milliseconds (optional)
   */
  set(key, value, ttl = null) {
    const expiration = Date.now() + (ttl || this.ttl);
    this.cache.set(key, { value, expiration });

    // If cache exceeds max size, remove oldest entry
    if (this.cache.size > this.maxSize) {
      const firstKey = this.cache.keys().next().value;
      this.cache.delete(firstKey);
    }
  }

  /**
   * Get a value from the cache
   * @param {string} key - Cache key
   * @returns {*} Cached value or undefined
   */
  get(key) {
    const item = this.cache.get(key);
    if (!item) {
      return undefined;
    }

    // Check if item has expired
    if (Date.now() > item.expiration) {
      this.cache.delete(key);
      return undefined;
    }

    return item.value;
  }

  /**
   * Check if a key exists in the cache
   * @param {string} key - Cache key
   * @returns {boolean} Whether key exists
   */
  has(key) {
    const item = this.cache.get(key);
    if (!item) {
      return false;
    }

    // Check if item has expired
    if (Date.now() > item.expiration) {
      this.cache.delete(key);
      return false;
    }

    return true;
  }

  /**
   * Delete a key from the cache
   * @param {string} key - Cache key
   * @returns {boolean} Whether deletion was successful
   */
  delete(key) {
    return this.cache.delete(key);
  }

  /**
   * Clear all cache entries
   */
  clear() {
    this.cache.clear();
  }

  /**
   * Get cache size
   * @returns {number} Number of cached entries
   */
  size() {
    return this.cache.size;
  }

  /**
   * Start periodic cleanup of expired entries
   */
  startCleanup() {
    this.cleanupTimer = setInterval(() => {
      this.cleanupExpired();
    }, this.cleanupInterval);
  }

  /**
   * Stop periodic cleanup
   */
  stopCleanup() {
    if (this.cleanupTimer) {
      clearInterval(this.cleanupTimer);
      this.cleanupTimer = null;
    }
  }

  /**
   * Manually cleanup expired entries
   */
  cleanupExpired() {
    const now = Date.now();
    for (const [key, item] of this.cache.entries()) {
      if (now > item.expiration) {
        this.cache.delete(key);
      }
    }
  }

  /**
   * Get cache statistics
   * @returns {Object} Cache stats
   */
  stats() {
    const now = Date.now();
    let validCount = 0;
    let expiredCount = 0;

    for (const item of this.cache.values()) {
      if (now > item.expiration) {
        expiredCount++;
      } else {
        validCount++;
      }
    }

    return {
      total: this.cache.size,
      valid: validCount,
      expired: expiredCount,
      maxSize: this.maxSize,
      utilization: (validCount / this.maxSize) * 100
    };
  }
}

// Singleton instance
const globalCache = new Cache({
  maxSize: 50,
  ttl: 10 * 60 * 1000, // 10 minutes
  cleanupInterval: 2 * 60 * 1000 // 2 minutes
});

export default globalCache;

// Specific cache instances for different use cases
export const apiCache = new Cache({
  maxSize: 100,
  ttl: 5 * 60 * 1000, // 5 minutes
  cleanupInterval: 60 * 1000 // 1 minute
});

export const userCache = new Cache({
  maxSize: 50,
  ttl: 15 * 60 * 1000, // 15 minutes
  cleanupInterval: 5 * 60 * 1000 // 5 minutes
});

export const taskCache = new Cache({
  maxSize: 200,
  ttl: 2 * 60 * 1000, // 2 minutes
  cleanupInterval: 30 * 1000 // 30 seconds
});