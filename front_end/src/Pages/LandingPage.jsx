import React from "react";
import { useState } from "react";
import { Link } from "react-router-dom";
import Navbar from "../Components/Navbar";

function LandingPage() {
  return (
    <>
    <Navbar/>
    
    <div>
      <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100 text-gray-800">
        <h1 className="text-3xl font-bold mb-6">Surv&Earn</h1>
      </div>
    </div>
    <Link to= "/"> LandingPage </Link>
    <Link to= "/AboutUs"> AboutUs </Link>
    <Link to= "/Login"> Login </Link>
    </>
  );
}

export default LandingPage;
