import { createBrowserRouter } from "react-router-dom";
import AppLayout from "../layout/AppLayout";
import Home from "../pages/Home";
import Settings from "../pages/Settings";
import Commands from "../pages/Commands";

export const router = createBrowserRouter([
    {
        path: "/",
        element: <AppLayout />,
        children: [
            { index: true, element: <Home /> },
            { path: "settings", element: <Settings /> },
            { path: "commands", element: <Commands /> },
        ],
    },
]);