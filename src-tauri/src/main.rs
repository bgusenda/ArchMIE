use serde::{Deserialize, Serialize};
use std::fs;
use std::process::Command;
use tauri::command;

#[derive(Debug, Serialize, Deserialize, Clone)]
#[serde(rename_all = "camelCase")]
struct CommandData {
    id: String,
    category: String,
    subcategory: String,
    title: String,
    command: String,
    description: String,
    isAdmin: bool,
}

#[derive(Debug, Serialize, Deserialize)]
struct CommandsFile {
    commands: Vec<CommandData>,
}

#[command]
fn read_commands_file() -> Result<CommandsFile, String> {
    let home_dir = dirs::home_dir()
        .ok_or("Não foi possível encontrar o diretório home")?;
    
    let commands_path = home_dir.join(".config").join("archmie").join("commands.json");
    
    if commands_path.exists() {
        let data = fs::read_to_string(&commands_path)
            .map_err(|e| format!("Erro ao ler arquivo: {}", e))?;
        
        let command_data: CommandsFile = serde_json::from_str(&data)
            .map_err(|e| format!("Erro ao parsear JSON: {}", e))?;
        
        Ok(command_data)
    } else {
        let default_commands = get_default_commands();
        
        if let Some(parent) = commands_path.parent() {
            fs::create_dir_all(parent).map_err(|e| format!("Erro ao criar diretório: {}", e))?;
        }
        
        let json = serde_json::to_string_pretty(&default_commands)
            .map_err(|e| format!("Erro ao serializar JSON: {}", e))?;
        
        fs::write(&commands_path, json)
            .map_err(|e| format!("Erro ao escrever arquivo: {}", e))?;
        
        Ok(default_commands)
    }
}

#[command]
fn write_commands_file(data: CommandsFile) -> Result<(), String> {
    let home_dir = dirs::home_dir()
        .ok_or("Não foi possível encontrar o diretório home")?;
    
    let commands_path = home_dir.join(".config").join("archmie").join("commands.json");
    
    let json = serde_json::to_string_pretty(&data)
        .map_err(|e| format!("Erro ao serializar JSON: {}", e))?;
    
    fs::write(commands_path, json)
        .map_err(|e| format!("Erro ao escrever arquivo: {}", e))?;
    
    Ok(())
}

#[command]
fn execute_command(command: String, isAdmin: bool) -> Result<String, String> {
    // Para comandos simples, ainda podemos simular
    let output = match command.as_str() {
        "sudo pacman -Syu" => "Sincronizando repositórios...\nAtualizando lista de pacotes...\nSistema atualizado com sucesso!",
        "sudo pacman -S" => "Por favor, especifique o nome do pacote. Exemplo: sudo pacman -S firefox",
        "pacman -Ss" => "Procurando pacotes...\nfirefox 115.0-1\nvim 9.0.2000-1\ngit 2.42.0-1\n...",
        "sudo pacman -Sc" => "Limpando cache...\nCache limpo com sucesso!",
        "uname -a" => "Linux archmie 6.5.0-arch1-1 #1 SMP PREEMPT_DYNAMIC Sat, 26 Aug 2023 07:30:17 +0000 x86_64 GNU/Linux",
        "df -h" => "Sist. Arq.      Tam. Usado Disp. Uso% Montado em\n/dev/nvme0n1p3  468G  256G  189G  58% /\ndevtmpfs        3,9G     0  3,9G   0% /dev",
        _ => &format!("Comando: {}\nUse 'Abrir no Terminal' para executar no terminal nativo", command)
    };
    
    println!("Simulando execução: {} (admin: {})", command, isAdmin);
    Ok(output.to_string())
}

#[command]
fn open_in_terminal(command: String) -> Result<(), String> {
    #[cfg(target_os = "linux")]
    {
        // Para Linux - executa o comando, verifica o status e exibe mensagem final antes de aguardar Enter
        let escaped = command.replace("\"", "\\\"");
        let wait_cmd = format!(
            "{}; status=$?; if [ $status -eq 0 ]; then echo \"\\nComando executado com sucesso (status $status).\"; else echo \"\\nComando falhou (status $status).\"; fi; echo \"\\nPressione Enter para fechar...\"; read -r",
            escaped
        );

        let terminals = [
            ("gnome-terminal", "--"),
            ("konsole", "-e"),
            ("xfce4-terminal", "-x"),
            ("xterm", "-e"),
            ("alacritty", "-e"),
            ("kitty", "-e"),
        ];

        for (t, a) in terminals.iter() {
            let terminal = *t;
            let arg = *a;

            if Command::new("which")
                .arg(terminal)
                .output()
                .map(|output| output.status.success())
                .unwrap_or(false)
            {
                let status = Command::new(terminal)
                    .arg(arg)
                    .arg("sh")
                    .arg("-c")
                    .arg(&wait_cmd)
                    .status()
                    .map_err(|e| format!("Erro ao abrir {}: {}", terminal, e))?;

                if status.success() {
                    return Ok(());
                }
            }
        }

        Err("Nenhum terminal encontrado. Terminais suportados: gnome-terminal, konsole, xfce4-terminal, xterm, alacritty, kitty".to_string())
    }

    #[cfg(target_os = "windows")]
    {
        // Para Windows - abre um cmd e mostra status, depois pede Enter (set /p)
        // Monta um comando que roda o comando original, testa %ERRORLEVEL% e então aguarda Enter.
        let win_cmd = format!(
            "{} & echo. & if %ERRORLEVEL%==0 (echo Comando executado com sucesso.) else (echo Comando falhou com codigo %ERRORLEVEL%) & echo. & set /p _=Pressione Enter para fechar...",
            command
        );

        Command::new("cmd")
            .args(["/C", "start", "cmd", "/K"])
            .arg(&win_cmd)
            .status()
            .map_err(|e| format!("Erro ao abrir terminal: {}", e))?;
        Ok(())
    }

    #[cfg(target_os = "macos")]
    {
        // Para macOS - usa AppleScript para pedir ao Terminal abrir e executar comando que checa o status e aguarda Enter
        let escaped = command.replace("\\", "\\\\").replace("\"", "\\\"");
        let wait_cmd = format!(
            "{}; status=$?; if [ $status -eq 0 ]; then echo \"\\nComando executado com sucesso (status $status).\"; else echo \"\\nComando falhou (status $status).\"; fi; echo \"\\nPressione Enter para fechar...\"; read -r",
            escaped
        );
        let script = format!(
            "tell application \"Terminal\" to do script \"{}\"",
            wait_cmd
        );

        Command::new("osascript")
            .args(["-e", &script])
            .status()
            .map_err(|e| format!("Erro ao abrir terminal: {}", e))?;
        Ok(())
    }
}

#[command]
fn app_exit() -> Result<(), String> {
    // Encerra o processo imediatamente.
    // Pode ser chamado a partir do frontend via invoke("app_exit")
    std::process::exit(0);
}

fn get_default_commands() -> CommandsFile {
    CommandsFile {
        commands: vec![
            CommandData {
                id: "1".to_string(),
                category: "Sistema".to_string(),
                subcategory: "Atualizar Sistema".to_string(),
                title: "Atualizar Sistema".to_string(),
                command: "sudo pacman -Syu".to_string(),
                description: "Atualiza todo o sistema e pacotes".to_string(),
                isAdmin: true,
            },
            CommandData {
                id: "2".to_string(),
                category: "Pacotes".to_string(),
                subcategory: "Instalar Pacote".to_string(),
                title: "Instalar Pacote".to_string(),
                command: "sudo pacman -S".to_string(),
                description: "Instala um pacote específico".to_string(),
                isAdmin: true,
            },
            CommandData {
                id: "3".to_string(),
                category: "Pacotes".to_string(),
                subcategory: "Procurar Pacote".to_string(),
                title: "Procurar Pacote".to_string(),
                command: "pacman -Ss".to_string(),
                description: "Procura por pacotes no repositório".to_string(),
                isAdmin: false,
            },
        ],
    }
}

fn main() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![
            read_commands_file,
            write_commands_file,
            execute_command,
            open_in_terminal,
            app_exit
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}