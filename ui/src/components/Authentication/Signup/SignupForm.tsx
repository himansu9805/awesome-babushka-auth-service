import React from "react";
import NeumorphButton from "@/components/commons/neumorph-button";
import { Link } from "react-router-dom";
import Divider from "@/components/commons/divider";

const SignupForm = () => {
  return (

    <div className="w-full max-w-md p-8 space-y-8 bg-white rounded-lg shadow-md">
      <h1 className="text-2xl font-bold text-left text-gray-700">
        Sign up to continue
      </h1>
      <form className="space-y-6">
        <div>
          <label htmlFor="name" className="block text-sm font-medium text-gray-700">
            Username
          </label>
          <input
            type="text"
            id="name"
            name="name"
            required
            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
          />
        </div>
        <div>
          <label htmlFor="email" className="block text-sm font-medium text-gray-700">
            Email address
          </label>
          <input
            type="email"
            id="email"
            name="email"
            required
            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
          />
        </div>
        <div>
          <label htmlFor="password" className="block text-sm font-medium text-gray-700">
            Password
          </label>
          <input
            type="password"
            id="password"
            name="password"
            required
            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
          />
        </div>
        <NeumorphButton fullWidth>Sign up</NeumorphButton>
        <div className="text-black text-xs mt-4 text-start w-full">
          By continuing, you agree to our <a href="#" className="text-blue-400 underline">Terms of Service</a>, <a href="#" className="text-blue-400 underline">Privacy Policy</a>, and <a href="#" className="text-blue-400 underline">Cookie Use</a>. Your privacy is our priority.
        </div>
      </form>
    </div>
  );
}

export default SignupForm;
