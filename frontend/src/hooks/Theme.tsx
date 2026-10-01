import { createContext, useContext, useState, type ReactNode } from "react";

type Theme = "light" | "dark";

type themeContextValue = {
  theme: Theme;
  toggleTheme: () => void;
  setTheme: (theme: Theme) => void;
}

const themeContext = createContext<themeContextValue>(null);

function getInitialTheme():Theme {
  if (typeof document === "undefined") return "dark";
  return (document.documentElement.getAttribute("data-theme") as Theme) ?? "dark";
}

export function ThemeProvider({children}: {children:ReactNode}) {
  const [theme, setTheme] = useState<Theme>(getInitialTheme);

  const toggleTheme = () => setTheme((prev) => (prev === "dark" ? "light" : "dark"));

  return(
    <themeContext.Provider value={{ theme, toggleTheme, setTheme }}>
      { children }
  </themeContext.Provider> )
}

export function useTheme() {
  const ctx = useContext(themeContext);
  if (!ctx) throw new Error("useTheme must be used in themeProvider");
  return ctx;
}
