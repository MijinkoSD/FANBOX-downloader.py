/// <reference no-default-lib="true" />
/// <reference lib="esnext" />
/// <reference lib="dom" />
/// <reference lib="dom.iterable" />


// @deno-types="https://denopkg.com/soremwar/deno_types/react/v16.13.1/react.d.ts"
import React from "https://dev.jspm.io/react";
// @deno-types="https://denopkg.com/soremwar/deno_types/react-dom/v16.13.1/react-dom.d.ts"
import ReactDOM from "https://dev.jspm.io/react-dom";

// ガーバッガガタキリッバッガタキリバ

import { sleep, getURLQuery, setURLQuery } from "./util.ts"


const a = <h1>Hello React!</h1>

const app = document.getElementById("app-test")
ReactDOM.render(a, app)

const urlpath:string = location.pathname
let urlparam:string = location.search
console.log(urlparam)
getURLQuery();



(async ()=>{
    await sleep(1500)
    setURLQuery([["a","1"],["bar","baz"]])
})()


