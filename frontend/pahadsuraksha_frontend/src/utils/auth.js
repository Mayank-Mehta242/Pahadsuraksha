export function getStoredToken(storage = globalThis.localStorage) {
  if (!storage) return "";

  const keys = ["token", "access_token", "authToken"];

  for (const key of keys) {
    const value = storage.getItem(key);
    if (value) {
      return value;
    }
  }

  return "";
}

export function storeAuthData(userData, authToken, storage = globalThis.localStorage) {
  if (!storage) return;

  if (authToken) {
    storage.setItem("token", authToken);
    storage.setItem("access_token", authToken);
    storage.setItem("authToken", authToken);
  }

  storage.setItem("user", JSON.stringify(userData || {}));
}

export function getStoredUser(storage = globalThis.localStorage) {
  if (!storage) return null;

  try {
    return JSON.parse(storage.getItem("user") || "null");
  } catch {
    return null;
  }
}

export function isAdminRole(role = "") {
  const normalizedRole = String(role || "").trim().toLowerCase();
  return normalizedRole.includes("official") || normalizedRole.includes("admin") || normalizedRole.includes("disaster");
}
