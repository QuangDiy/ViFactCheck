// contexts/GlobalContext.js

import { createContext, useState } from 'react';

export const GlobalContext = createContext();

export function GlobalContextProvider({ children }) {
  const [globalVar, setGlobalVar] = useState('initial value');

  function updateGlobalVar(newValue) {
    setGlobalVar(newValue);
  }

  return (
    <GlobalContext.Provider 
      value={{ 
        globalVar, 
        updateGlobalVar 
      }}
    >
      {children}
    </GlobalContext.Provider>
  )
}