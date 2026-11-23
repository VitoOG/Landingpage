const test = require("node:test");
const assert = require("node:assert/strict");
const vm = require("node:vm");
const fs = require("node:fs");
const source = fs.readFileSync("js/order-core.js", "utf8");
function makeStore(seed) {
  const store = new Map(seed ? [["ggc-service-request-v1", seed]] : []);
  const context = {window:{}, localStorage:{
    getItem:k=>store.get(k)??null,
    setItem:(k,v)=>store.set(k,v)
  }};
  vm.runInNewContext(source, context);
  return {api:context.window.GGCOrderCore,store};
}
test("empty cart is safe",()=>{const {api}=makeStore();assert.deepEqual(Array.from(api.read()),[]);});
test("add deduplicates",()=>{const {api}=makeStore();const a=api.add([], "SE-01");assert.deepEqual(Array.from(api.add(a,"SE-01")),["SE-01"]);});
test("invalid ids and malformed storage are discarded",()=>{const {api}=makeStore("{broken");assert.deepEqual(Array.from(api.read()),[]);assert.deepEqual(Array.from(api.add([],"garbage")),[]);});
test("valid ids persist and duplicates are normalized",()=>{const {api,store}=makeStore(JSON.stringify(["SE-01","SE-01","BAD","SE-33"]));assert.deepEqual(Array.from(api.read()),["SE-01","SE-33"]);api.write(["SE-02"]);assert.equal(JSON.parse(store.get("ggc-service-request-v1"))[0],"SE-02");});
test("remove is deterministic",()=>{const {api}=makeStore();assert.deepEqual(Array.from(api.remove(["SE-01","SE-02"],"SE-01")),["SE-02"]);});
