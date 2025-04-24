import React, { useState, useContext } from "react"
import { useForm } from "react-hook-form";
import NeumorphButton from "@/components/commons/neumorph-button";
import { environment } from "@/environments/environment";
import axios from "axios";
import Spinner from "@/components/animated/Spinner";
import { AuthContext } from "@/contexts/AuthContext";

type FormData = {
  username: string;
  password: string;
};

const SigninForm = () => {
  const {
    register,
    handleSubmit,
    formState: { errors, touchedFields }
  } = useForm<FormData>();
  const [formError, setFormError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const { setUser } = useContext(AuthContext);

  const onSubmit = (data: FormData) => {
    setIsLoading(true);
    axios.post(
      `${environment.services.auth}/auth/login`,
      data,
      { withCredentials: true }
    )
      .then(response => {
        setFormError(null);
        setUser(response.data);
        console.log("Login successful:", response.data);
      })
      .catch(error => {
        setFormError(error.response?.data.error || "An error occurred");
      })
      .finally(() => {
        setIsLoading(false);
      });
  };

  return (
    <div className="w-full max-w-md p-8 space-y-6">
      <h1 className="text-2xl font-bold text-left text-gray-700">
        Sign in to continue
      </h1>
      <form className="space-y-5" onSubmit={handleSubmit(onSubmit)} noValidate>
        {formError && (
          <div className="text-red-600 text-sm mb-2">{formError}</div>
        )}
        <div>
          <label htmlFor="username" className="block text-sm font-medium text-gray-700">
            Username
          </label>
          <input
            type="text"
            id="username"
            {...register("username", {
              required: "Username is required"
            })}
            className={`mt-1 block w-full px-3 py-2 border ${errors.username && touchedFields.username ? "border-red-500" : "border-gray-300"
              } rounded-md shadow-sm focus:outline-none focus:ring-[#36322F] focus:border-[#36322F] sm:text-sm`}
          />
          {errors.username && touchedFields.username && (
            <p className="text-xs text-red-500 mt-1">{errors.username.message}</p>
          )}
        </div>
        <div>
          <label htmlFor="password" className="block text-sm font-medium text-gray-700">
            Password
          </label>
          <input
            type="password"
            id="password"
            {...register("password", {
              required: "Password is required",
              minLength: {
                value: 6,
                message: "Password must be at least 6 characters"
              }
            })}
            className={`mt-1 block w-full px-3 py-2 border ${errors.password && touchedFields.password ? "border-red-500" : "border-gray-300"
              } rounded-md shadow-sm focus:outline-none focus:ring-[#36322F] focus:border-[#36322F] sm:text-sm`}
          />
          {errors.password && touchedFields.password && (
            <p className="text-xs text-red-500 mt-1">{errors.password.message}</p>
          )}
        </div>
        <NeumorphButton fullWidth type="submit" className="mt-8" disabled={isLoading}>
          {isLoading ? (
            <Spinner />
          ) : (
            "Sign in"
          )}
        </NeumorphButton>
        <div className="text-black text-xs mt-4 text-start w-full">
          By continuing, you agree to our <a href="#" className="text-blue-400 underline">Terms of Service</a>, <a href="#" className="text-blue-400 underline">Privacy Policy</a>, and <a href="#" className="text-blue-400 underline">Cookie Use</a>. Your privacy is our priority.
        </div>
      </form>
    </div>
  );
}

export default SigninForm;
