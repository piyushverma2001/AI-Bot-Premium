import React from "react";
import Chat from "./Chat";
import "./App.css"; // Import CSS file for styling

/**
 * App component that serves as the root of the application.
 * Provides a layout with a header, main chat area, and footer.
 */
function App() {
  return (
    <div className="app-container">
      <header className="app-header">
        <h1>ChatBot Assistant</h1>
      </header>
      <main className="app-main">
        <Chat />
      </main>
      <footer className="app-footer">
        <p>© {new Date().getFullYear()} ChatBot Inc.</p>
      </footer>
    </div>
  );
}

export default App;
