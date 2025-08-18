import React from "react";
import { Link } from "react-scroll";

const Navbar = () => {
    return (
        <nav className="fixed top-0 left-0 w-full bg-white shadow p-4 flex gap-6 z-50">
            <Link
                to="Home"
                smooth={true}
                duration={500}
                className="cursor-pointer hover:text-blue-500"
            >
                Home
            </Link>
            <Link
                to="HowItWorks"
                smooth={true}
                duration={500}
                className="cursor-pointer hover:text-blue-500"
            >
                About
            </Link>
            <Link
                to="AboutUs"
                smooth={true}
                duration={500}
                className="cursor-pointer hover:text-blue-500"
            >
                How-It-Works
            </Link>
        </nav>
    );
};

export default Navbar;
