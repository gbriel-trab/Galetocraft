<#
"PC de mentira" para o benchmark do Pirococó.

Espera o processo do jogo (cliente de desenvolvimento do Fabric) aparecer e:
  1. se -Nucleos > 0: prende o jogo a esse número de núcleos físicos (um processador lógico por núcleo: 0,2,4,...);
  2. se -Velocidade < 100: põe "queimadores" (threads que só fazem conta) presos nesses mesmos núcleos, com a mesma
     prioridade do jogo. O Windows divide cada núcleo por igual entre o jogo e os queimadores, então TODA thread do
     jogo (inclusive a que desenha a tela) roda a ~Velocidade% da velocidade: 1 queimador por núcleo = 50%,
     2 = 33%, 3 = 25%. Vale só para esses núcleos e só enquanto o jogo estiver aberto; nada no sistema é alterado.
  3. mede, a cada segundo, o uso do motor 3D da GPU por esse processo e o uso de CPU dele, num CSV.
O benchmark.sh também avisa o Java do jogo que ele só tem N processadores (-XX:ActiveProcessorCount), como num PC de N núcleos.

Uso: powershell -File sandbox_pc.ps1 -Saida medicao.csv [-Nucleos 4 -Velocidade 50]
#>
param(
    [Parameter(Mandatory = $true)][string]$Saida,
    [int]$Nucleos = 0,
    [int]$Velocidade = 100,
    [int]$EsperaMaxSeg = 600
)

Add-Type -TypeDefinition @"
using System;
using System.Runtime.InteropServices;
using System.Threading;
public static class Queimador {
    [DllImport("kernel32.dll")] static extern IntPtr GetCurrentThread();
    [DllImport("kernel32.dll")] static extern UIntPtr SetThreadAffinityMask(IntPtr t, UIntPtr mascara);
    public static volatile bool Parar = false;
    public static int Iniciar(int[] cpus, int porCpu) {
        int n = 0;
        foreach (int c in cpus) {
            for (int k = 0; k < porCpu; k++) {
                int cpu = c;
                Thread t = new Thread(() => {
                    SetThreadAffinityMask(GetCurrentThread(), (UIntPtr)(1UL << cpu));
                    double x = 0;
                    while (!Parar) { x += Math.Sqrt(x + 1.0); if (x > 1e12) x = 0; }
                });
                t.IsBackground = true;
                t.Priority = ThreadPriority.Normal;
                t.Start();
                n++;
            }
        }
        return n;
    }
}
"@

$logicos = (Get-CimInstance Win32_Processor | Measure-Object -Property NumberOfLogicalProcessors -Sum).Sum
$inicio = Get-Date
$jogo = $null
while (-not $jogo -and ((Get-Date) - $inicio).TotalSeconds -lt $EsperaMaxSeg) {
    $jogo = Get-CimInstance Win32_Process -Filter "Name='java.exe' or Name='javaw.exe'" |
        Where-Object { $_.CommandLine -like '*fabric.dli.env=client*' -or $_.CommandLine -like '*devlaunchinjector*' } |
        Select-Object -First 1
    if (-not $jogo) { Start-Sleep -Milliseconds 300 }
}
if (-not $jogo) { Write-Output "jogo não apareceu"; exit 1 }
$pid_jogo = [int]$jogo.ProcessId
Write-Output "jogo encontrado: pid $pid_jogo"

if ($Nucleos -gt 0) {
    $mascara = 0; $cpus = @()
    for ($i = 0; $i -lt $Nucleos; $i++) { $mascara = $mascara -bor (1 -shl (2 * $i)); $cpus += (2 * $i) }
    (Get-Process -Id $pid_jogo).ProcessorAffinity = [IntPtr]$mascara
    $porCpu = 0
    if ($Velocidade -lt 100) { $porCpu = [int][math]::Round(100.0 / $Velocidade) - 1 }
    $n = 0
    if ($porCpu -gt 0) { $n = [Queimador]::Iniciar([int[]]$cpus, $porCpu) }
    Write-Output ("limite: {0} núcleos (lógicos {1}), {2} queimador(es) por núcleo -> jogo com ~{3}% de cada núcleo ({4} threads)" -f `
        $Nucleos, ($cpus -join ','), $porCpu, [math]::Round(100.0 / ($porCpu + 1)), $n)
}

"tempo_ms,gpu3d_jogo,gpu3d_total,cpu_jogo_maquina" | Out-File -FilePath $Saida -Encoding ascii
$proc = Get-Process -Id $pid_jogo
$cpuAntes = $proc.TotalProcessorTime.TotalMilliseconds
$tAntes = Get-Date
while (-not $proc.HasExited) {
    $amostra = Get-Counter '\GPU Engine(*engtype_3D)\Utilization Percentage' -ErrorAction SilentlyContinue
    $jogoGpu = 0.0; $total = 0.0
    if ($amostra) {
        foreach ($s in $amostra.CounterSamples) {
            $total += $s.CookedValue
            if ($s.InstanceName -like "pid_$($pid_jogo)_*") { $jogoGpu += $s.CookedValue }
        }
    }
    $proc.Refresh()
    if ($proc.HasExited) { break }
    $agora = Get-Date
    $cpu = $proc.TotalProcessorTime.TotalMilliseconds
    $cpuPct = 100.0 * ($cpu - $cpuAntes) / (($agora - $tAntes).TotalMilliseconds * $logicos)
    $cpuAntes = $cpu; $tAntes = $agora
    $ms = [DateTimeOffset]::new($agora).ToUnixTimeMilliseconds()
    [string]::Format([Globalization.CultureInfo]::InvariantCulture, "{0},{1:F2},{2:F2},{3:F2}", $ms, $jogoGpu, $total, $cpuPct) |
        Out-File -FilePath $Saida -Append -Encoding ascii
    Start-Sleep -Milliseconds 700
}
[Queimador]::Parar = $true
Write-Output "jogo terminou"
