// Commands.tsx
import { useState, useEffect, useCallback } from "react";
import { invoke } from "@tauri-apps/api/core";
import { Save, Edit3, Trash2, Shield, User, X, Plus, Terminal } from "lucide-react";
import "./Commands.scss";

interface Command {
  id: string;
  category: string;
  subcategory: string;
  title: string;
  command: string;
  description: string;
  isAdmin: boolean;
}

interface CommandData {
  commands: Command[];
}

export default function Commands() {
  const [commands, setCommands] = useState<Command[]>([]);
  const [output, setOutput] = useState<string>("");
  const [editingCommand, setEditingCommand] = useState<Command | null>(null);
  const [editForm, setEditForm] = useState({ 
    title: "", 
    command: "", 
    description: "",
    category: "",
    subcategory: "" 
  });
  const [activeCategory, setActiveCategory] = useState("Todos");
  const [isLoading, setIsLoading] = useState(false);

  // diagnóstico: ver se componente monta e capturar erros globais
  const [mountError, setMountError] = useState<string | null>(null);
  useEffect(() => {
    console.log("Commands mounted");
    const onError = (ev: ErrorEvent) => {
      console.error("Uncaught error:", ev.error || ev.message);
      setMountError(String(ev.error || ev.message));
    };
    const onRejection = (ev: PromiseRejectionEvent) => {
      console.error("Unhandled rejection:", ev.reason);
      setMountError(String(ev.reason));
    };
    window.addEventListener("error", onError);
    window.addEventListener("unhandledrejection", onRejection);
    return () => {
      window.removeEventListener("error", onError);
      window.removeEventListener("unhandledrejection", onRejection);
    };
  }, []);

  // type guard to validate commands array
  const isCommandArray = (value: unknown): value is Command[] => {
    return Array.isArray(value) && value.every(item => typeof item === 'object' && item !== null && 'id' in item && 'command' in item);
  };

  // Carregar comandos do JSON com fallback para cache local
  const loadCommands = useCallback(async () => {
    try {
      const response = await invoke("read_commands_file") as unknown;
      // Normalizar formatos: backend pode retornar { commands: [...] } ou array puro
      let cmds: Command[] | null = null;

      if (isCommandArray(response)) {
        cmds = response;
      } else if (response && typeof response === 'object' && 'commands' in (response as Record<string, unknown>)) {
        const maybe = (response as Record<string, unknown>).commands;
        if (isCommandArray(maybe)) cmds = maybe;
      }

      const finalCmds: Command[] = cmds ?? getDefaultCommands();
      setCommands(cmds);
      localStorage.setItem("archmie-commands", JSON.stringify({ commands: finalCmds }));
    } catch (error) {
      console.error("Erro ao carregar comandos:", error);
      const stored = localStorage.getItem("archmie-commands");
      if (stored) {
        try {
          const parsed = JSON.parse(stored) as CommandData;
          if (Array.isArray(parsed.commands)) {
            setCommands(parsed.commands);
            return;
          }
        } catch (e) {
          console.error("Erro ao parsear cache local:", e);
        }
      }
      setCommands(getDefaultCommands());
    }
  }, []);

  useEffect(() => { loadCommands(); }, [loadCommands]);

  const getDefaultCommands = (): Command[] => [
    {
      id: "1",
      category: "Sistema",
      subcategory: "Atualizar Sistema",
      title: "Atualizar Sistema",
      command: "sudo pacman -Syu",
      description: "Atualiza todo o sistema e pacotes",
      isAdmin: true
    },
    {
      id: "2",
      category: "Pacotes",
      subcategory: "Instalar Pacote",
      title: "Instalar Pacote",
      command: "sudo pacman -S",
      description: "Instala um pacote específico",
      isAdmin: true
    },
    {
      id: "3",
      category: "Pacotes",
      subcategory: "Procurar Pacote",
      title: "Procurar Pacote",
      command: "pacman -Ss",
      description: "Procura por pacotes no repositório",
      isAdmin: false
    },
    {
      id: "4",
      category: "Sistema",
      subcategory: "Limpar Cache",
      title: "Limpar Cache",
      command: "sudo pacman -Sc",
      description: "Limpa o cache de pacotes",
      isAdmin: true
    },
    {
      id: "5",
      category: "Informações",
      subcategory: "Informações do Sistema",
      title: "Ver Informações do Sistema",
      command: "uname -a",
      description: "Mostra informações detalhadas do sistema",
      isAdmin: false
    },
    {
      id: "6",
      category: "Informações",
      subcategory: "Espaço em Disco",
      title: "Ver Espaço em Disco",
      command: "df -h",
      description: "Mostra o uso de espaço em disco",
      isAdmin: false
    }
  ];

  const saveCommands = async (updatedCommands: Command[]) => {
    try {
      await invoke("write_commands_file", { commands: updatedCommands });
      setCommands(updatedCommands);
      localStorage.setItem("archmie-commands", JSON.stringify({ commands: updatedCommands }));
    } catch (error) {
      console.error("Erro ao salvar comandos (fallback local):", error);
      localStorage.setItem("archmie-commands", JSON.stringify({ commands: updatedCommands }));
      setCommands(updatedCommands);
    }
  };

  const executeCommand = async (command: string, isAdmin: boolean) => {
    setIsLoading(true);
    setOutput("Executando comando...");

    try {
      const result = await invoke("execute_command", {
        command,
        // enviar snake_case para compatibilidade com bindings Rust/Tauri
        is_admin: isAdmin,
      } as Record<string, unknown>);

      // normalize response
      const out = typeof result === "string" ? result : JSON.stringify(result, null, 2);
      setOutput(out);
    } catch (error) {
      console.error("Erro executeCommand:", error);
      setOutput(`Erro ao executar comando: ${String(error)}`);
    } finally {
      setIsLoading(false);
    }
  };

  // Adicionei esta nova função
  const openInTerminal = async (command: string) => {
    try {
      await invoke("open_in_terminal", { command });
      setOutput(`Comando enviado para o terminal nativo: ${command}`);
    } catch (error) {
      setOutput(`Erro ao abrir terminal: ${error}`);
    }
  };
  
  const handleEdit = (command: Command) => {
    setEditingCommand(command);
    setEditForm({
      title: command.title,
      command: command.command,
      description: command.description,
      category: command.category,
      subcategory: command.subcategory
    });
  };

  const handleSaveEdit = () => {
    if (!editingCommand) return;

    const updatedCommands = commands.map(cmd =>
      cmd.id === editingCommand.id
        ? { 
            ...cmd, 
            title: editForm.title,
            command: editForm.command,
            description: editForm.description,
            category: editForm.category,
            subcategory: editForm.subcategory
          }
        : cmd
    );

    // Se for um novo comando
    if (editingCommand.id.startsWith("new-")) {
      updatedCommands.push({
        ...editingCommand,
        title: editForm.title,
        command: editForm.command,
        description: editForm.description,
        category: editForm.category,
        subcategory: editForm.subcategory,
        id: Date.now().toString()
      });
    }

    saveCommands(updatedCommands);
    setEditingCommand(null);
    setEditForm({ 
      title: "", 
      command: "", 
      description: "",
      category: "",
      subcategory: "" 
    });
  };

  const handleDelete = (commandId: string) => {
    if (window.confirm("Tem certeza que deseja deletar este comando?")) {
      const updatedCommands = commands.filter(cmd => cmd.id !== commandId);
      saveCommands(updatedCommands);
    }
  };

  const handleAddCommand = () => {
    const newCommand: Command = {
      id: "new-" + Date.now(),
      category: "Personalizado",
      subcategory: "Meus Comandos",
      title: "Novo Comando",
      command: "echo 'Hello World'",
      description: "Descrição do novo comando",
      isAdmin: false
    };
    
    setEditingCommand(newCommand);
    setEditForm({
      title: "Novo Comando",
      command: "echo 'Hello World'",
      description: "Descrição do novo comando",
      category: "Personalizado",
      subcategory: "Meus Comandos"
    });
  };

  const categories = ["Todos", ...new Set(commands.map(cmd => cmd.category))];
  const filteredCommands = activeCategory === "Todos"
    ? commands
    : commands.filter(cmd => cmd.category === activeCategory);

  const groupedCommands = filteredCommands.reduce((acc, cmd) => {
    if (!acc[cmd.subcategory]) {
      acc[cmd.subcategory] = [];
    }
    acc[cmd.subcategory].push(cmd);
    return acc;
  }, {} as Record<string, Command[]>);

  // Antes do return, mostrar erro se capturado
  if (mountError) {
    return (
      <div style={{ padding: 20, color: "#fff", background: "#111", minHeight: "100vh" }}>
        <h2>Erro no frontend</h2>
        <pre style={{ whiteSpace: "pre-wrap", color: "#f88" }}>{mountError}</pre>
        <p>Abra as devtools (Ctrl+Shift+I) e verifique o console para mais detalhes.</p>
      </div>
    );
  }

  return (
    <div className="commands">
      {/* Hero Section */}
      <section className="commands__hero">
        <h1 className="commands__title">Terminal ArchMIE</h1>
        <p className="commands__subtitle">
          Execute e gerencie comandos Arch Linux com segurança e praticidade
        </p>
      </section>

      {/* Navegação por Categorias */}
      <nav className="commands__nav">
        {categories.map(category => (
          <button
            key={category}
            className={`commands__nav-btn ${activeCategory === category ? 'active' : ''}`}
            onClick={() => setActiveCategory(category)}
          >
            {category}
          </button>
        ))}
        <button
          className="commands__nav-btn"
          onClick={handleAddCommand}
          style={{
            background: 'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)',
            color: '#000',
            display: 'flex',
            alignItems: 'center',
            gap: '0.5rem'
          }}
        >
          <Plus size={16} />
          Novo Comando
        </button>
      </nav>

      {/* Lista de Comandos */}
      {Object.entries(groupedCommands).map(([subcategory, subCommands]) => (
        <section key={subcategory} className="commands__section">
          <h2 className="commands__section-title">{subcategory}</h2>

          {subCommands.map((cmd) => (
            <div key={cmd.id} style={{ marginBottom: '2.5rem' }}>
              <h3 className="commands__subsection-title">{cmd.title}</h3>
              <p style={{ color: 'rgba(255, 255, 255, 0.7)', marginBottom: '1rem' }}>
                {cmd.description}
              </p>

              <div className="commands__code">
                {cmd.command}
              </div>

              <div className="commands__actions">
                <button
                  className="commands__btn commands__btn--edit"
                  onClick={() => handleEdit(cmd)}
                >
                  <Edit3 size={16} />
                  EDITAR
                </button>
                <button
                  className="commands__btn commands__btn--delete"
                  onClick={() => handleDelete(cmd.id)}
                >
                  <Trash2 size={16} />
                  DELETAR
                </button>
                {/* Adicionado: botão para abrir no terminal nativo */}
                <button
                  className="commands__btn"
                  onClick={() => openInTerminal(cmd.command)}
                  style={{
                    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
                  }}
                >
                  <Terminal size={16} />
                  ABRIR NO TERMINAL
                </button>
              </div>

              <div className="commands__actions">
                <button
                  className="commands__btn commands__btn--admin"
                  onClick={() => executeCommand(cmd.command, true)}
                  disabled={isLoading}
                >
                  <Shield size={16} />
                  EXECUTAR COMO ADMIN
                </button>
                <button
                  className="commands__btn commands__btn--user"
                  onClick={() => executeCommand(cmd.command, false)}
                  disabled={isLoading}
                >
                  <User size={16} />
                  EXECUTAR COMOUSUÁRIO
                </button>
              </div>
            </div>
          ))}
        </section>
      ))}

      {/* Output do Terminal */}
      <section className="commands__section">
        <h2 className="commands__section-title">
          Output do Terminal {isLoading && "⏳"}
        </h2>
        <div className="commands__execution">
          <div className="commands__output">
            {output || (
              <div className="commands__output-placeholder">
                {isLoading
                  ? "Executando comando..."
                  : "O output dos comandos aparecerá aqui..."
                }
              </div>
            )}
          </div>
        </div>
      </section>

      {/* Modal de Edição */}
      {editingCommand && (
        <div className="commands__modal">
          <div className="commands__modal-content">
            <h3 className="commands__modal-title">
              {editingCommand.id.startsWith("new-") ? "Novo Comando" : "Editar Comando"}
            </h3>
            
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem', marginBottom: '1rem' }}>
              <input
                type="text"
                placeholder="Categoria"
                value={editForm.category}
                onChange={(e) => setEditForm({...editForm, category: e.target.value})}
                className="commands__input"
              />
              <input
                type="text"
                placeholder="Subcategoria"
                value={editForm.subcategory}
                onChange={(e) => setEditForm({...editForm, subcategory: e.target.value})}
                className="commands__input"
              />
            </div>

            <input
              type="text"
              placeholder="Título do comando"
              value={editForm.title}
              onChange={(e) => setEditForm({...editForm, title: e.target.value})}
              className="commands__input"
            />
            
            <textarea
              placeholder="Comando (ex: sudo pacman -Syu)"
              value={editForm.command}
              onChange={(e) => setEditForm({...editForm, command: e.target.value})}
              className="commands__textarea"
              
            />
            
            <input
              type="text"
              placeholder="Descrição"
              value={editForm.description}
              onChange={(e) => setEditForm({...editForm, description: e.target.value})}
              className="commands__input"
            />

            <div style={{ marginBottom: '1rem' }}>
              <label style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: 'rgba(255, 255, 255, 0.8)' }}>
                <input
                  type="checkbox"
                  checked={editingCommand.isAdmin}
                  onChange={(e) => setEditingCommand({
                    ...editingCommand,
                    isAdmin: e.target.checked
                  })}
                />
                Requer privilégios de administrador (sudo)
              </label>
            </div>

            <div className="commands__actions">
              <button 
                className="commands__btn commands__btn--save"
                onClick={handleSaveEdit}
              >
                <Save size={16} />
                {editingCommand.id.startsWith("new-") ? "CRIAR COMANDO" : "SALVAR ALTERAÇÕES"}
              </button>
              <button 
                className="commands__btn commands__btn--exit"
                onClick={() => setEditingCommand(null)}
              >
                <X size={16} />
                CANCELAR
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}