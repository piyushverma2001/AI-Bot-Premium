import { render, screen } from "@testing-library/react";
import App from "./App";

test("renders ChatBot Assistant header", () => {
  render(<App />);
  // Check that the header with the text "ChatBot Assistant" is present
  const headerElement = screen.getByText(/chatbot assistant/i);
  expect(headerElement).toBeInTheDocument();
});

test("renders footer with ChatBot Inc.", () => {
  render(<App />);
  // Check that the footer contains the expected text
  const footerElement = screen.getByText(/ChatBot Inc/i);
  expect(footerElement).toBeInTheDocument();
});
