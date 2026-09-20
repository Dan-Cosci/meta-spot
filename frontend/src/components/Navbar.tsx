import Logo from "../assets/meta-spot-logo.svg"

export default function Navbar() {
  return (
    <nav className="max-md:px-4 md:px-[10vw] py-4 flex flex-row justify-between items-center">
      <div className="flex flex-row justify-between items-center gap-3">
        <img src={Logo} alt="meta spot logo" className="max-md:w-12  md:w-14" />
        <h2 className="font-bold max-md:text-2xl md: text-2xl">Meta-spot</h2>
      </div>
      <div className="flex flex-row justify-between items-center gap-5">
        <p className="text-lg hover:text-green-300">home</p>
        <p className="text-lg hover:text-green-300">about</p>
      </div>
    </nav>
  );
}
