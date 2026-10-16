
import React, { useState } from "react";

function Register() {
  const [formData, setFormData] = useState({
    username: "",
    first_name: "",
    last_name: "",
    email: "",
    password: "",
  });

  const [message, setMessage] = useState("");

  const handleChange = (event) => {
    setFormData({
      ...formData,
      [event.target.name]: event.target.value,
    });
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setMessage("");

    try {
      const response = await fetch("/api/register/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      });

      const data = await response.json();

      if (response.ok) {
        setMessage(data.message || "Registration successful!");
        setFormData({
          username: "",
          first_name: "",
          last_name: "",
          email: "",
          password: "",
        });
      } else {
        setMessage(data.error || data.detail || "Registration failed.");
      }
    } catch (error) {
      setMessage("Unable to connect to the server. Please try again.");
    }
  };

  return (
    <div className="register-container">
      <div className="register-card">
        <h1>Create an Account</h1>
        <p className="register-subtitle">
          Join Cars Dealership to explore dealers and share reviews.
        </p>

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="username">Username</label>
            <input
              id="username"
              name="username"
              type="text"
              placeholder="Enter username"
              value={formData.username}
              onChange={handleChange}
              autoComplete="username"
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="first_name">First Name</label>
            <input
              id="first_name"
              name="first_name"
              type="text"
              placeholder="Enter first name"
              value={formData.first_name}
              onChange={handleChange}
              autoComplete="given-name"
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="last_name">Last Name</label>
            <input
              id="last_name"
              name="last_name"
              type="text"
              placeholder="Enter last name"
              value={formData.last_name}
              onChange={handleChange}
              autoComplete="family-name"
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="email">Email</label>
            <input
              id="email"
              name="email"
              type="email"
              placeholder="Enter email address"
              value={formData.email}
              onChange={handleChange}
              autoComplete="email"
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              id="password"
              name="password"
              type="password"
              placeholder="Enter password"
              value={formData.password}
              onChange={handleChange}
              autoComplete="new-password"
              minLength={8}
              required
            />
          </div>

          <button className="register-button" type="submit">
            Register
          </button>
        </form>

        {message && (
          <p className="register-message" role="status">
            {message}
          </p>
        )}
      </div>
    </div>
  );
}

export default Register;
