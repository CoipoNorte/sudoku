const express = require('express');
const fs = require('fs');
const path = require('path');
const router = express.Router();

const scorePath = path.join(__dirname, '..', 'data', 'score.json');

// Obtener puntaje
router.get('/', (req, res) => {
  if (fs.existsSync(scorePath)) {
    const data = fs.readFileSync(scorePath, 'utf8');
    res.json(JSON.parse(data));
  } else {
    res.json({ easy: 0, medium: 0, hard: 0 });
  }
});

// Guardar puntaje
router.post('/', (req, res) => {
  fs.writeFileSync(scorePath, JSON.stringify(req.body));
  res.json({ status: 'ok' });
});

module.exports = router;