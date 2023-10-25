import React, { useState, useRef, useEffect } from 'react';
import './styles/text_editor.css';
import { CommandToAPI } from '../utils/apiRequests';


function Text_editor() {
    const [filePath, setFilePath] = useState(''); // Estado para el nombre del archivo
    const [commands, setCommands] = useState(''); // Estado para los comandos
    const [output, setOutput] = useState(''); // Estado para el resultado
    const [paused, setPaused] = useState(false);

    const fileInputRef = useRef(null);

    async function execute_script() {
        let tempOutput = ''; // Variable temporal para acumular el resultado

        const script_commands = commands.trim().split('\n');
        for (const command of script_commands) {
            setOutput(tempOutput); // Actualizar el estado output
            if (command.startsWith("#")) {
                tempOutput += command.slice(1) + '\n'; // Agregar comentario a la variable temporal
                setOutput(tempOutput);
                continue;
            }
            const tokens = command.split(' ');
            switch (tokens[0].toLowerCase()) {
                
                case 'mkdisk':
                    tempOutput += "\n∟ Comando MKDISK\n";
                    try {
                        const data = await CommandToAPI('mkdisk', tokens)
                        console.log(data)
                        tempOutput += data['Message'] + '\n'
                        setOutput(tempOutput); // Actualiza el estado
                    } catch (error) {
                        console.error('Error:', error)
                    }
                    break

                case 'rmdisk':
                    tempOutput += "\n∟ Comando RMDISK\n"
                    const ask = window.confirm("¿Desea eliminar el disco?")
                    if(ask){
                        try{
                            const data = await CommandToAPI('rmdisk', tokens)
                            console.log(data)
                            tempOutput += data['Message'] + '\n'
                            setOutput(tempOutput); // Actualiza el estado
                        }catch(error){
                            console.error('Error:', error)
                        }
                    }else{
                        tempOutput += "∟ Operación cancelada\n"
                        setOutput(tempOutput); // Actualiza el estado
                    }
                    break

                case 'fdisk':
                    tempOutput += "\n∟ Comando FDISK\n"
                    try{
                        const data = await CommandToAPI('fdisk', tokens)
                        console.log(data)
                        tempOutput += data['Message'] + '\n'
                        setOutput(tempOutput); // Actualiza el estado
                    }catch(error){
                        console.error('Error:', error)
                    }
                    break
                case 'mount':
                    tempOutput += "\n∟ Comando MOUNT\n"
                    try{
                        const data = await CommandToAPI('mount', tokens)
                        console.log(data)
                        tempOutput += data['Message'] + '\n'
                        setOutput(tempOutput); // Actualiza el estado
                    }catch(error){
                        console.error('Error:', error)
                    }
                    break
                case 'unmount':
                    tempOutput += "\n∟ Comando UNMOUNT\n"
                    try{
                        const data = await CommandToAPI('unmount', tokens)
                        console.log(data)
                        tempOutput += data['Message'] + '\n'
                        setOutput(tempOutput); // Actualiza el estado
                    }catch(error){
                        console.error('Error:', error)
                    }
                    break
                case 'rep':
                    tempOutput += "\n∟ Comando REP\n"
                    try{
                        const data = await CommandToAPI('rep', tokens)
                        console.log(data)
                        tempOutput += data['Message'] + '\n'
                        setOutput(tempOutput); // Actualiza el estado
                    }catch(error){
                        console.error('Error:', error)
                    }
                    break
                case 'pause':

                    tempOutput += "\n∟ Aplicación en pausa, presione enter para continuar\n"
                    alert("Aplicación en pausa, presione aceptar para continuar")
                    setPaused(true)
                    
                    break
                default:
                    console.log(`[Error] Comando ${tokens[0]} no reconocido.`)
                    break
            }
        }

    }


    const handleFileChooser = () => {
        fileInputRef.current.click();
    }
    const handleFileChange = (e) => {
        const file = e.target.files[0]; // Obtiene el archivo seleccionado
        if (file) {
            const reader = new FileReader();

            reader.onload = (e) => {
                const content = e.target.result;
                setFilePath(file.name);
                setCommands(content);
            }
            reader.readAsText(file);
        }
    }

    return (
        <div id="page-wrapper" className="clearfix">
            <h1>Aplicación de comandos</h1>
            <p>Powered by Christopher Monterroso.</p>
            <div className="field">
                <input type="text" readOnly name="filename" id="filename" placeholder="Cargue su archivo .mia" value={filePath} />
                <button type="button" onClick={handleFileChooser}>Cargar archivo</button>
                <input
                    type="file"
                    accept=".mia"
                    ref={fileInputRef}
                    style={{ display: 'none' }} // Oculta el input de tipo file
                    onChange={handleFileChange}
                />
            </div>
            <div className="field">
                <textarea
                    name="content"
                    id="content"
                    placeholder="Ingrese los comandos aquí (1 comando por línea)."
                    value={commands}
                    onChange={(e) => setCommands(e.target.value)}
                ></textarea>
            </div>
            <div className="field">
                <button type="button" onClick={execute_script}>Ejecutar</button>
                {//<button type="submit">Continuar</button>
                }
            </div>


            <div id="files-four">
                <h2>Resultado</h2>
                <textarea readOnly value={output} style={{ width: '100%', minHeight: '100px' }} />
            </div>
        </div>
    );
}

export default Text_editor;
