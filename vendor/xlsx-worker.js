/* Reads spreadsheets in a separate worker: whatever a crafted file does to the parser stays here,
   away from the logged-in page, and the page can stop it if it takes too long. */
importScripts('xlsx.full.min.js');
onmessage = function(e){
  try {
    var wb = XLSX.read(e.data, { type: 'array', cellFormula: false, cellHTML: false, cellStyles: false, bookVBA: false });
    var names = wb.SheetNames.slice(0, 30), sheets = {};
    names.forEach(function(n){
      var rows = XLSX.utils.sheet_to_json(wb.Sheets[n], { header: 1, raw: true, defval: '' }).slice(0, 20000);
      sheets[n] = rows.map(function(r){ return r.slice(0, 60).map(function(c){ return (typeof c === 'number' || typeof c === 'boolean') ? c : String(c).slice(0, 300); }); });
    });
    postMessage({ names: names, sheets: sheets });
  } catch (err) { postMessage({ error: String(err && err.message || err) }); }
};
