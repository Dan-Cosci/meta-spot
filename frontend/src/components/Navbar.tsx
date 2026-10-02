import { useTheme } from "@/hooks/Theme";
import Logo from "../assets/meta-spot-logo.svg"

export default function Navbar() {
  const { toggleTheme } = useTheme()

  return (
    <nav className="max-md:px-4 md:px-[10vw] py-4 flex flex-row justify-between items-center">
      <div className="flex flex-row justify-between items-center gap-3">
        <img src={Logo} alt="meta spot logo" className="max-md:w-12  md:w-14" />
        <h2 className="font-bold max-md:text-2xl text-2xl">Meta-spot</h2>
      </div>
      <div className="flex flex-row justify-between items-center gap-5">
        <p className="text-lg hover:text-green-300" onClick={() => toggleTheme()}></p>
        <p className="text-lg hover:text-green-300">Home</p>
        <p className="text-lg hover:text-green-300">Downloads</p>
      </div>
    </nav>
  );
}
