import { createBrowserRouter } from "react-router-dom";
import RootLayout from "./layouts/RootLayout";
import Download from "./features/Download";
import Dashboard from "./features/Dashboard";


const App = createBrowserRouter([
  {
    path: "/",
    Component: RootLayout,
    children: [
      { index: true, Component: Download },
      { path:"dashboard", Component: Dashboard }
    ]

  }
])

export default App;
