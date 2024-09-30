"use client";
import React, {
  createContext,
  useContext,
  useReducer,
  useEffect,
  ReactNode,
} from "react";

// Define the state type
interface BooleanState {
  isToggled: boolean;
}

// Define the action types
type Action = { type: "toggle" };

// Define the initial state
const initialState: BooleanState = {
  isToggled: false,
};

// Create a reducer function
const booleanReducer = (state: BooleanState, action: Action): BooleanState => {
  switch (action.type) {
    case "toggle":
      return { ...state, isToggled: !state.isToggled };
    default:
      return state;
  }
};

// Create the context
const BooleanContext = createContext<
  | {
      state: BooleanState;
      dispatch: React.Dispatch<Action>;
    }
  | undefined
>(undefined);

// Create a provider component
export const BooleanProvider: React.FC<{ children: ReactNode }> = ({
  children,
}) => {
  // Load the initial state from localStorage or fallback to initialState
  const [state, dispatch] = useReducer(
    booleanReducer,
    initialState,
    (initial) => {
      if (typeof window !== "undefined") {
        const localData = localStorage.getItem("isToggled");
        return localData ? { isToggled: JSON.parse(localData) } : initial;
      }
      return initial; // This is for SSR when window is undefined
    }
  );

  // Save the state to localStorage whenever it changes (only client-side)
  useEffect(() => {
    if (typeof window !== "undefined") {
      localStorage.setItem("isToggled", JSON.stringify(state.isToggled));
    }
  }, [state.isToggled]);

  return (
    <BooleanContext.Provider value={{ state, dispatch }}>
      {children}
    </BooleanContext.Provider>
  );
};

// Create a custom hook for easy access to the context
export const useBooleanContext = () => {
  const context = useContext(BooleanContext);
  if (context === undefined) {
    throw new Error("useBooleanContext must be used within a BooleanProvider");
  }
  return context;
};
