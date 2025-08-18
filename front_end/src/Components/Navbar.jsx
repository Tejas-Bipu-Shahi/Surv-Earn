import React, { useState } from "react";
import { Link, useLocation } from "react-router-dom";

const Navbar = () => {
    const location = useLocation();
    const [showDropDown, setShowDropDown] = useState(false);

    return (
        <nav className="bg-white dark:bg-gray-900 fixed w-full z-20 top-0 left-0 border-b border-gray-200 dark:border-gray-600">
            <div className="max-w-screen-xl flex flex-wrap items-center justify-between mx-auto p-4">

                {/* Buttons */}
                <div className="flex md:order-2 space-x-3 md:space-x-0 rtl:space-x-reverse">
                    <Link to="/login">
                        <button className="text-gray-900 bg-white border border-gray-300 focus:outline-none hover:bg-gray-100 focus:ring-4 focus:ring-gray-100 font-medium rounded-full text-sm px-5 py-2.5 dark:bg-gray-800 dark:text-white dark:border-gray-600 dark:hover:bg-gray-700">
                            Login
                        </button>
                    </Link>
                </div>

                {/* Nav Links */}
                <div className="items-center justify-between hidden w-full md:flex md:w-auto md:order-1">
                    <ul className="flex flex-col p-4 md:p-0 mt-4 font-medium border border-gray-100 rounded-lg bg-gray-50 md:flex-row md:mt-0 md:border-0 md:bg-white dark:bg-gray-800 md:dark:bg-gray-900 dark:border-gray-700 md:space-x-8 rtl:space-x-reverse">
                        <li>
                            <Link
                                to="/"
                                className={`block py-2 px-3 rounded-sm hover:bg-gray-100 md:p-0 dark:text-white ${location.pathname === "/" ? "text-blue-600 md:text-blue-500" : ""
                                    }`}
                            >
                                HOME
                            </Link>
                        </li>
                        <li>
                            <Link
                                to="/about-us"
                                className={`block py-2 px-3 rounded-sm hover:bg-gray-100 md:p-0 dark:text-white ${location.pathname === "/about-us" ? "text-blue-600 md:text-blue-500" : ""
                                    }`}
                            >
                                ABOUT US
                            </Link>
                        </li>
                        <li
                            onMouseEnter={() => setShowDropDown(true)}
                            onMouseLeave={() => setShowDropDown(false)}
                            className="relative block py-2 px-3 rounded-sm hover:bg-gray-100 md:p-0 dark:text-white cursor-pointer"
                        >
                            SERVICES
                            {showDropDown && (
                                <div className="absolute mt-2 bg-white dark:bg-gray-700 shadow-md rounded-lg w-44 z-10">
                                    <ul className="py-2 text-sm text-gray-700 dark:text-gray-200">
                                        <li>
                                            <Link
                                                to="/service1"
                                                className="block px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-600 dark:hover:text-white"
                                            >
                                                Service 1
                                            </Link>
                                        </li>
                                        <li>
                                            <Link
                                                to="/service2"
                                                className="block px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-600 dark:hover:text-white"
                                            >
                                                Service 2
                                            </Link>
                                        </li>
                                        <li>
                                            <Link
                                                to="/service3"
                                                className="block px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-600 dark:hover:text-white"
                                            >
                                                Service 3
                                            </Link>
                                        </li>
                                    </ul>
                                </div>
                            )}
                        </li>
                        <li>
                            <Link
                                to="/contact"
                                className={`block py-2 px-3 rounded-sm hover:bg-gray-100 md:p-0 dark:text-white ${location.pathname === "/contact" ? "text-blue-600 md:text-blue-500" : ""
                                    }`}
                            >
                                CONTACT
                            </Link>
                        </li>
                    </ul>
                </div>
            </div>
        </nav>
    );
};

export default Navbar;
