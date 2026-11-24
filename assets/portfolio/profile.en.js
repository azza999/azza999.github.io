// Match translations by the original title, so reordering projects is safe.
window.portfolioEnglish = {
  name: 'Dohyun Kim',
  projects: {
    'Autobounty': {
      summary: 'LLM-powered framework for automated open-source vulnerability analysis',
      description: 'I built a framework that automates repository exploration, vulnerability analysis, independent verification, and report writing. Initially focused on finding vulnerabilities, it evolved to validate exploitability in real-world environments, assess downstream impact, and verify vulnerability chains.',
      result: '22 audits · 10 external reports · 3 published GHSAs'
    },
    'CodexTF': {
      summary: 'Hypothesis-driven multi-agent framework for solving CTF challenges',
      description: 'To address reasoning stalls in a single LLM agent and duplicated exploration during parallel execution, I designed a system that decomposes challenges into hypotheses and coordinates agents with distinct roles. I refined it to separate individual hypothesis testing from end-to-end attack-chain reproduction and to verify state continuity between tasks.',
      result: 'Solved 9 of 13 Jeopardy challenges at CCE 2026'
    },
    'CCE 2026 SpeedHack Solver': {
      summary: 'Real-time automated solving pipeline for time-limited CTF challenges',
      description: 'I automated challenge collection, LLM-based solving, and flag submission for problems released roughly every 15 minutes. I optimized the workflow to reduce collection delays and unnecessary decision steps, continuously improving performance throughout the competition.',
      result: '15 first solves · 3rd of 50 SpeedHack teams · Average solve time of 1 min 58 sec over the final 11 rounds'
    },
    'MCRC 성능개량사업': {
      title: 'MCRC System Upgrade',
      summary: 'Defense command-and-control system upgrade, operational testing, and security planning',
      description: 'Drawing on experience operating the existing MCRC command-and-control system since 2020, I reviewed system requirements and project deliverables after the upgrade began. From late 2024, I participated in validating new equipment installation, approving work, and preparing operating procedures and backup and recovery guidelines. As an operational test and evaluation officer, I wrote and refined procedures to assess requirements, consolidated overlapping procedures, and led test execution. I also handled technical vulnerability analysis, security control implementation, security assessments, and follow-up actions through revalidation and reporting.',
      result: 'Key experience · Improved redundancy failure tests · Identified and verified missing firewall policies · Operational readiness and security planning',
      note: 'Recruiters and hiring managers may request a detailed portfolio by personal email. After reviewing the request, I can share further materials within the limits of what may be disclosed.'
    },
    '497.1일 이후 발생한 HP-UX 장애': {
      title: 'An HP-UX Failure After 497.1 Days',
      summary: 'Tracing an MPT/SCSI driver timer issue on long-running servers',
      description: 'I investigated MPT/SCSI errors and a surge in system logs on HP-UX servers after extended uptime. Comparing logs and reboot histories across three identical servers revealed that only the recently rebooted server was operating normally. I reviewed driver documentation and found that the symptoms were consistent with a 32-bit timer overflow occurring after approximately 497.1 days.',
      result: 'HP-UX · MPT/SCSI · syslog analysis · Reboot history comparison · Investigation of a 497.1-day timer overflow'
    },
    '이중화에 관한 고찰': {
      title: 'Rethinking Redundancy',
      summary: 'Analyzing a redundancy failure involving HSRP and vSphere recovery policies',
      description: 'Failover worked when one backbone switch was shut down, but restoring it caused a system-wide communication outage. I investigated network convergence, including MAC updates, RARP, and STP, as a possible cause when HSRP preemption and vSphere failback occurred together. The issue did not recur after automatic vSphere failback was disabled. This reinforced the need to test recovery behavior as well as failover when designing redundancy.',
      result: 'HSRP · vSphere · Failover/failback · Recovery-stage outage analysis · No recurrence observed after configuration change'
    }
  }
};
