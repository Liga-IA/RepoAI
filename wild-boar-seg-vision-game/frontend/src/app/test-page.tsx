export default function TestPage() {
  return (
    <div style={{ 
      backgroundColor: '#0a1a0f', 
      color: 'white', 
      minHeight: '100vh',
      padding: '20px'
    }}>
      <h1 style={{ fontSize: '48px', color: 'white' }}>TESTE - JAVALI HUNTER</h1>
      <p style={{ color: 'white' }}>Se você está vendo isso, o problema é com o CSS/Tailwind</p>
      <button style={{ 
        backgroundColor: '#16a34a', 
        color: 'white', 
        padding: '10px 20px',
        fontSize: '20px',
        border: 'none',
        borderRadius: '5px',
        cursor: 'pointer'
      }}>
        BOTÃO DE TESTE
      </button>
    </div>
  )
}

