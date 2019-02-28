export function useFormInput(initialValue) {
    const [value, setValue] = useState(initialValue);
  
    function onChangeHandler(event) {
      setValue(event.target.value);
    }
  
    return {
      value,
      onChange: onChangeHandler
    };
}

// Exmaple Usage:
// 
// function App() {
//     const name = useFormInput("");
  
//     return (
//       <div className="App">
//         <input {...name} />
//         <h2>Start editing to see some magic happen!</h2>
//       </div>
//     );
//   }`