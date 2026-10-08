import { useTheme } from "@/hooks/Theme";
import { Link, useLocation } from "react-router";
import { DarkThemeLogo, LightThemeLogo } from "@/config/constant";
import { IoMoon, IoSunny } from "react-icons/io5";

export default function Navbar() {
  const { toggleTheme, theme } = useTheme()

  const location = useLocation()

  return (
    <nav className="max-md:px-4 md:px-[10vw] py-4 flex flex-row justify-between items-center">
      <div className="flex flex-row justify-between items-center gap-3">
        <img src={theme == "dark" ? DarkThemeLogo: LightThemeLogo} alt="meta spot logo" className="w-12 md:w-10" />
        <h2 className="font-bold max-md:text-2xl text-2xl">Meta-spot</h2>
      </div>
      <div className="flex flex-row justify-between items-center gap-5">
        <p
          className="text-2xl rounded-full p-1 hover:bg-main/20 btn-animation transition-colors duration-75"
          onClick={() => toggleTheme()}>{theme === "dark" ? <IoSunny /> : <IoMoon />}
        </p>
        <p className="text-lg hover:text-main"><Link to={location.pathname === "/" ? "/downloads" : "/"}>{ location.pathname == "/"? "Downloads" : "Home"}</Link></p>
      </div>
    </nav>
  );
}
