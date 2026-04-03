#!/usr/bin/env python3
"""
version_manager.py — Leader Skill 版本管理器
管理 leaders/ 目录下各 Leader 的版本历史与升级
"""

import json
import shutil
import sys
from datetime import datetime
from pathlib import Path

# ─── 配置 ──────────────────────────────────────────────────────────────────────

LEADERS_DIR = Path(__file__).parent.parent / "leaders"
VERSIONS_DIR = Path(__file__).parent.parent / ".versions"

# ─── 核心类 ────────────────────────────────────────────────────────────────────


class VersionManager:
    """
    管理 leaders/{name}/ 目录的版本快照。

    版本格式：v{major}.{minor}
    - major 升级：性格基调改变（用户主动触发）
    - minor 升级：话术细节修正（correction_handler 触发）

    快照存储在 .versions/{leader_dir}/{version}/ 目录中
    """

    def __init__(self, leader_dir: str):
        self.leader_dir = LEADERS_DIR / leader_dir
        self.version_dir = VERSIONS_DIR / leader_dir

        if not self.leader_dir.exists():
            raise FileNotFoundError(f"Leader 目录不存在: {self.leader_dir}")

        self.version_dir.mkdir(parents=True, exist_ok=True)

    # ── 版本读取 ───────────────────────────────────────────────────────────────

    def current_version(self) -> str:
        """读取当前版本号"""
        meta_path = self.leader_dir / "meta.json"
        if meta_path.exists():
            with open(meta_path, encoding="utf-8") as f:
                meta = json.load(f)
            return meta.get("version", "v1.0")
        return "v1.0"

    def list_versions(self) -> list[dict]:
        """列出所有历史版本"""
        versions = []
        for vdir in sorted(self.version_dir.iterdir()):
            if not vdir.is_dir():
                continue
            log_path = vdir / "changelog.json"
            entry = {"version": vdir.name, "path": str(vdir)}
            if log_path.exists():
                with open(log_path, encoding="utf-8") as f:
                    log = json.load(f)
                entry.update(log)
            versions.append(entry)
        return versions

    def get_changelog(self) -> list[dict]:
        """读取版本变更日志"""
        changelog_path = self.version_dir / "CHANGELOG.json"
        if changelog_path.exists():
            with open(changelog_path, encoding="utf-8") as f:
                return json.load(f)
        return []

    # ── 版本创建 ───────────────────────────────────────────────────────────────

    def snapshot(self, bump: str = "minor", reason: str = "") -> str:
        """
        创建当前版本的快照，并升级版本号。
        bump = 'minor' | 'major'
        返回新版本号
        """
        current = self.current_version()
        new_version = self._bump_version(current, bump)

        # 创建快照目录
        snapshot_dir = self.version_dir / current
        snapshot_dir.mkdir(exist_ok=True)

        # 复制三个文件
        for filename in ("meta.json", "persona.md", "work.md"):
            src = self.leader_dir / filename
            if src.exists():
                shutil.copy2(src, snapshot_dir / filename)

        # 写变更日志
        log_entry = {
            "version": current,
            "saved_at": datetime.now().isoformat(),
            "reason": reason,
            "bump_type": bump,
        }
        changelog_file = snapshot_dir / "changelog.json"
        changelog_file.write_text(json.dumps(log_entry, ensure_ascii=False, indent=2), encoding="utf-8")

        # 更新全局 CHANGELOG.json
        self._append_changelog(log_entry)

        # 升级 meta.json 中的版本号
        self._write_version(new_version)

        return new_version

    def restore(self, version: str) -> bool:
        """从历史版本恢复"""
        restore_from = self.version_dir / version
        if not restore_from.exists():
            print(f"❌ 版本不存在: {version}")
            return False

        for filename in ("meta.json", "persona.md", "work.md"):
            src = restore_from / filename
            if src.exists():
                shutil.copy2(src, self.leader_dir / filename)

        print(f"✅ 已从 {version} 恢复")
        return True

    def diff(self, v1: str, v2: str) -> None:
        """简单对比两个版本的 meta.json"""
        dir1 = self.version_dir / v1
        dir2 = self.version_dir / v2

        for fname in ("meta.json",):
            p1 = dir1 / fname
            p2 = dir2 / fname
            if not p1.exists() or not p2.exists():
                continue

            with open(p1, encoding="utf-8") as f:
                d1 = json.load(f)
            with open(p2, encoding="utf-8") as f:
                d2 = json.load(f)

            print(f"\n── {fname} 差异: {v1} → {v2} ──")
            all_keys = set(d1.keys()) | set(d2.keys())
            for key in sorted(all_keys):
                val1 = d1.get(key, "（无）")
                val2 = d2.get(key, "（无）")
                if val1 != val2:
                    print(f"  {key}:")
                    print(f"    {v1}: {val1}")
                    print(f"    {v2}: {val2}")

    # ── 工具函数 ───────────────────────────────────────────────────────────────

    def _bump_version(self, version: str, bump: str) -> str:
        """v1.2 → v1.3 (minor) 或 v2.0 (major)"""
        match = version.lstrip("v").split(".")
        major, minor = int(match[0]), int(match[1]) if len(match) > 1 else 0
        if bump == "major":
            return f"v{major + 1}.0"
        return f"v{major}.{minor + 1}"

    def _write_version(self, new_version: str) -> None:
        """更新 meta.json 中的 version 字段"""
        meta_path = self.leader_dir / "meta.json"
        if meta_path.exists():
            with open(meta_path, encoding="utf-8") as f:
                meta = json.load(f)
            meta["version"] = new_version
            meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")

    def _append_changelog(self, entry: dict) -> None:
        changelog_path = self.version_dir / "CHANGELOG.json"
        existing: list = []
        if changelog_path.exists():
            with open(changelog_path, encoding="utf-8") as f:
                existing = json.load(f)
        existing.append(entry)
        changelog_path.write_text(json.dumps(existing, ensure_ascii=False, indent=2), encoding="utf-8")


# ─── CLI 入口 ──────────────────────────────────────────────────────────────────


def main():
    commands = {
        "snapshot": "创建版本快照（升级版本号）",
        "restore":  "从历史版本恢复",
        "list":     "列出所有历史版本",
        "diff":     "对比两个版本的差异",
    }

    if len(sys.argv) < 3:
        print("用法: python version_manager.py <leader目录名> <命令> [参数...]")
        print("示例:")
        print("  python version_manager.py example_ali_p10 list")
        print("  python version_manager.py example_ali_p10 snapshot minor '修正话术语气'")
        print("  python version_manager.py example_ali_p10 diff v1.0 v1.1")
        print("  python version_manager.py example_ali_p10 restore v1.0")
        print("\n支持命令:")
        for cmd, desc in commands.items():
            print(f"  {cmd:10s}  {desc}")
        sys.exit(1)

    leader_dir = sys.argv[1]
    command = sys.argv[2]

    try:
        vm = VersionManager(leader_dir)
    except FileNotFoundError as e:
        print(f"❌ {e}")
        sys.exit(1)

    if command == "list":
        versions = vm.list_versions()
        if not versions:
            print("暂无历史版本（当前为初始状态）")
        else:
            print(f"\n{leader_dir} 版本历史（共 {len(versions)} 个快照）：")
            for v in versions:
                print(f"  {v['version']:8s}  {v.get('saved_at', '')[:10]}  {v.get('reason', '')}")

    elif command == "snapshot":
        bump = sys.argv[3] if len(sys.argv) > 3 else "minor"
        reason = sys.argv[4] if len(sys.argv) > 4 else ""
        old_ver = vm.current_version()
        new_ver = vm.snapshot(bump=bump, reason=reason)
        print(f"✅ 快照创建成功：{old_ver} → {new_ver}")

    elif command == "restore":
        if len(sys.argv) < 4:
            print("❌ 请指定要恢复的版本，如: restore v1.0")
            sys.exit(1)
        vm.restore(sys.argv[3])

    elif command == "diff":
        if len(sys.argv) < 5:
            print("❌ 请指定两个版本，如: diff v1.0 v1.1")
            sys.exit(1)
        vm.diff(sys.argv[3], sys.argv[4])

    else:
        print(f"❌ 未知命令: {command}")
        print(f"支持: {', '.join(commands.keys())}")
        sys.exit(1)


if __name__ == "__main__":
    main()
