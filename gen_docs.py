import os
import shutil
import yaml

DOCS_DIR = "docs"
PROJECTS_DIR = "_temp"


def delete_docs_subdirs():
    docs_path = os.path.join(os.getcwd(), DOCS_DIR)
    if os.path.exists(docs_path):
        for item in os.listdir(docs_path):
            item_path = os.path.join(docs_path, item)
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)

def copy_projects():
    projects_path = os.path.join(os.getcwd(), PROJECTS_DIR)
    docs_path = os.path.join(os.getcwd(), DOCS_DIR)

    if os.path.exists(projects_path):
        for vehicle in os.listdir(projects_path):
            vehicle_src = os.path.join(projects_path, vehicle)
            if os.path.isdir(vehicle_src):
                vehicle_dst = os.path.join(docs_path, vehicle)
                os.makedirs(vehicle_dst, exist_ok=True)

                for project in os.listdir(vehicle_src):
                    project_src = os.path.join(vehicle_src, project)
                    if os.path.isdir(project_src):
                        project_dst = os.path.join(vehicle_dst, project)
                        os.makedirs(project_dst, exist_ok=True)

                        for file in os.listdir(project_src):
                            src_file = os.path.join(project_src, file)
                            if file.lower().endswith(".html"):
                                dst_file = os.path.join(project_dst, "model.html")
                                shutil.copy2(src_file, dst_file)
                            elif file.lower().endswith(".pdf"):
                                dst_file = os.path.join(project_dst, "guide.pdf")
                                shutil.copy2(src_file, dst_file)

def generate_docs_and_nav():
    nav = []

    # Walk through vehicles
    for vehicle in sorted(os.listdir(DOCS_DIR)):
        vehicle_path = os.path.join(DOCS_DIR, vehicle)
        if os.path.isdir(vehicle_path):
            vehicle_nav = []

            # Walk through projects
            for project in sorted(os.listdir(vehicle_path)):
                project_path = os.path.join(DOCS_DIR, vehicle, project)
                if os.path.isdir(project_path):
                    # Determine original file paths
                    pdf_orig = next((f for f in os.listdir(project_path) if f.lower().endswith(".pdf")), None)
                    html_orig = next((f for f in os.listdir(project_path) if f.lower().endswith(".html")), None)

                    # Define new file names with underscores
                    pdf_name = f"{vehicle}_{project}_guide.pdf"
                    html_name = f"{vehicle}_{project}_model.html"

                    # Rename files if they exist
                    if pdf_orig:
                        os.rename(os.path.join(project_path, pdf_orig),
                                  os.path.join(project_path, pdf_name))
                    if html_orig:
                        os.rename(os.path.join(project_path, html_orig),
                                  os.path.join(project_path, html_name))

                    pdf_exists = os.path.exists(os.path.join(project_path, pdf_name))
                    html_exists = os.path.exists(os.path.join(project_path, html_name))

                    # Generate index.md for the project
                    md_content = f"# {project} Harness Guide\n\n"

                    # Material attr_list buttons
                    if pdf_exists:
                        md_content += f"[Open PDF]({pdf_name}){{: .md-button .md-raised target=\"_blank\" }}\n\n"
                    if html_exists:
                        md_content += f"[Open 3D Model]({html_name}){{: .md-button .md-raised target=\"_blank\" }}\n\n"

                    # Write index.md
                    index_md_path = os.path.join(project_path, "index.md")
                    with open(index_md_path, "w", encoding="utf-8") as f:
                        f.write(md_content)

                    # Add project to vehicle nav
                    vehicle_nav.append({project: f"{vehicle}/{project}/index.md"})

            # Add vehicle to nav if it has projects
            if vehicle_nav:
                nav.append({vehicle: vehicle_nav})

    # Generate mkdocs.yml
    mkdocs_config = {
        "site_name": "Wire Harnessing Docs",
        "theme": {
            "name": "material",
            "palette": [
                {"scheme": "slate", "primary": "blue"}
            ]
        },
        "nav": nav,
        "markdown_extensions": ["attr_list"]
    }

    with open("mkdocs.yml", "w", encoding="utf-8") as f:
        yaml.dump(mkdocs_config, f, sort_keys=False)

    print("Auto-generated project pages with renamed files (underscores) and mkdocs.yml successfully.")

if __name__ == "__main__":
    delete_docs_subdirs()
    copy_projects()
    generate_docs_and_nav()

