import React from 'react'
import Navbar from "../Components/Navbar";
import Home from './Home';
import AboutUs from './AboutUs';
import HowItWorks from './HowItWorks';

function LandingPage() {
  return (
    <>
      <Navbar/>
      <h1>Tejas</h1>
      <Home/>
      <HowItWorks/>
      <AboutUs/>
      

    </>
  );
}

export default LandingPage;
