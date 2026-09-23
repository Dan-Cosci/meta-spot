import Footer from "@/components/Footer";
import Navbar from "@/components/Navbar";
import { Outlet } from "react-router";

export const RootLayout = () => {
	return (
	  <>
      <div className="min-h-screen min-w-screen bg-neutral-900 text-white flex flex-col">
        <Navbar />
        <main className="h-full flex-1 max-md:px-4 md:px-[10vw] flex flex-col items-center text-center max-md:pt-10 pt-18">
          <Outlet />
        </main>
      </div>
      <Footer />

    </>
	);
};

export default RootLayout;
