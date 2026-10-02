import { createBrowserRouter } from "react-router";
import RootLayout from "./layouts/RootLayout";
import Download from "./features/Download";
import Dashboard from "./features/Dashboard";


const App = createBrowserRouter([
  {
    path: "/",
    Component: RootLayout,
    children: [
      { index: true, Component: Dashboard },
      { path: "download", Component: Download }
    ]

  }
])

export default App;
