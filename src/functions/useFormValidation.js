function useFormValidation(initialValue, options) {
  const [value, setValue] = useState(initialValue);
  const [errors, setErrors] = useState([]);
  const [dirty, setDirty] = useState(false);

  function checkForErrors(value) {
    const newErrors = [];

    if (options.minLength && value.length < options.minLength) {
      newErrors.push(`You need a minimum of ${options.minLength} characters`);
    }

    if (options.minLength && value.length > options.maxLength) {
      newErrors.push(
        `You have exceeded the max characters of ${options.maxLength}`
      );
    }

    if (options.required && value.length === 0) {
      newErrors.push("This field is required");
    }

    setErrors(newErrors);
  }

  function onChangeHandler(event) {
    const { value } = event.target;
    setValue(value);

    if (dirty) {
      checkForErrors(value);
    }
  }

  function onBlurHandler() {
    setDirty(true);
  }

  return {
    value,
    errors,
    onBlur: onBlurHandler,
    onChange: onChangeHandler
  };
}

// Example
// 
// function App() {
//   const { errors, ...name } = useFormValidation("", {
//     required: true,
//     minLength: 3,
//     maxLength: 6
//   });

//   return (
//     <div className="App">
//       <input {...name} />
//       {errors.map(nameError => (
//         <p>{nameError}</p>
//       ))}

//       <h5>The value of name: {name.value}</h5>
//     </div>
//   );
// }