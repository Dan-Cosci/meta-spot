import Logo from "../assets/meta-spot-logo.svg"

export default function Footer() {
  return (
    <footer className="bg-neutral-950 border-t border-neutral-800">
      <div className="max-md:px-4 md:px-[10vw] py-10">
        {/* Grid: 1 column on mobile, 4 on desktop */}
        <div className="grid grid-cols-1 gap-8 md:grid-cols-4 md:gap-6">

          {/* Brand */}
          <div className="flex flex-col gap-3">
            <div className="flex flex-row items-center gap-2">
              <img src={Logo} alt="meta spot logo" className="w-8" />
              <span className="font-bold">Meta-spot</span>
            </div>
            <p className="text-sm text-neutral-500">
              Make your MP3s complete with metadata and cover art.
            </p>
          </div>

          {/* Product links */}
          <div className="flex flex-col gap-2">
            <h3 className="text-sm font-semibold text-neutral-400 uppercase tracking-wider mb-1">
              Product
            </h3>
            {/* TODO: add real hrefs */}
            <a href="#" className="text-sm text-neutral-500 hover:text-green-300 transition-colors">Home</a>
            <a href="#" className="text-sm text-neutral-500 hover:text-green-300 transition-colors">How it works</a>
            <a href="#" className="text-sm text-neutral-500 hover:text-green-300 transition-colors">Changelog</a>
            {/* TODO: add pricing/features links if applicable */}
          </div>

          {/* Legal links */}
          <div className="flex flex-col gap-2">
            <h3 className="text-sm font-semibold text-neutral-400 uppercase tracking-wider mb-1">
              Legal
            </h3>
            {/* TODO: add real hrefs */}
            <a href="#" className="text-sm text-neutral-500 hover:text-green-300 transition-colors">Terms of Service</a>
            <a href="#" className="text-sm text-neutral-500 hover:text-green-300 transition-colors">Privacy Policy</a>
            <a href="#" className="text-sm text-neutral-500 hover:text-green-300 transition-colors">Disclaimer</a>
          </div>

          {/* Socials */}
          <div className="flex flex-col gap-2">
            <h3 className="text-sm font-semibold text-neutral-400 uppercase tracking-wider mb-1">
              Connect
            </h3>
            {/* TODO: add real social links */}
            <a href="#" className="text-sm text-neutral-500 hover:text-green-300 transition-colors">GitHub</a>
            <a href="#" className="text-sm text-neutral-500 hover:text-green-300 transition-colors">X / Twitter</a>
            <a href="#" className="text-sm text-neutral-500 hover:text-green-300 transition-colors">Discord</a>
            {/* TODO: add more socials (YouTube, Bluesky, etc.) */}
          </div>
        </div>

        {/* Bottom bar */}
        <div className="border-t border-neutral-800 mt-8 pt-6 flex max-md:flex-col md:flex-row justify-between items-center gap-2">
          <p className="text-xs text-neutral-600">
            © {new Date().getFullYear()} Meta-spot. For personal use.
          </p>
          {/* TODO: replace with your GitHub repo link */}
          <a href="#" className="text-xs text-neutral-600 hover:text-green-300 transition-colors">
            Open source on GitHub
          </a>
        </div>
      </div>
    </footer>
  );
}
