import requests
import urllib.parse
from typing import Optional

class IdwallAuth:
    
    """
    A class used to authenticate idwall token and account, besides getting API status and user profile.

    Attributes:
        auth (Auth): An instance of the Auth class used for authentication.

    Methods:
        make_request: makes an API request.

    """
    
    def __init__(self, token):
        """
        Initializes an instance of IdwallAuth.

        Args:
            token (str): The authentication token.

        Attributes:
            base_url (str): The base URL for API requests.
            token (str): The authentication token.
            headers (dict): The headers for API requests, including the authorization token.
        """
        self.base_url = "https://api-v2.idwall.co/"
        self.token = token
        self.headers = {
            "Content-Type" : "application/json",
            'Authorization': self.token
            }

    def make_request(self, method, endpoint, data=None, params=None):
        """
        Makes an API request.

        Args:
            method (str): The HTTP method for the request (e.g., 'GET', 'POST', 'PUT', 'DELETE').
            endpoint (str): The API endpoint.
            data (dict, optional): The request payload data (JSON format).
            params (dict, optional): The query parameters for the request.

        Returns:
            requests.Response: The response object from the API request.
        """
            
        url = urllib.parse.urljoin(self.base_url, endpoint)
        response = requests.request(method, url, headers=self.headers, json=data, params=params)
        # Check if the response status code is 200 (OK)
            
        try:
            response.raise_for_status()
            return response.json()
        except requests.HTTPError as e:
            raise e
        
    def get_api_status(self):
        """
        Retrieves the status of API.
        
        Args:
            
        Returns:
            The status of API.
        """
        endpoint = 'status'
        return self.make_request('GET', endpoint)
    
    def get_user_profile(self):
        """
        Retrieves the infos of an account.
        
        Args:
            
        Returns:
            Infos of an account.
        """
        endpoint = 'usuario'
        return self.make_request('GET', endpoint)
    
class Matrices:
    
    """
    A class representing a collection of matrices.

    Attributes:
        auth (Auth): An instance of the Auth class used for authentication.

    Methods:
        list_matrices: Retrieves the list of registrered matrices.
        get_matrix_details: Retrieves the details of a specific matrix.

    """
    
    base_matrices = 'matrizes'
    
    def __init__(self, auth: IdwallAuth):
        """
        Initializes a Matrices object with IdwallAuth for authentication.

        Args:
            auth (IdwallAuth): An authentication object used for making requests.
        """
        self.auth = auth

    def list_matrices(self):
        """
        Retrieves a list of matrices.
        
        Returns:
            A list of matrices.
        """
        return self.auth.make_request('GET', self.base_matrices)

    def get_matrix_details(self, matrix_id):
        """
        Retrieves the details of a specific matrix.
        
        Args:
            matrix_id (str): The ID of the matrix.
            
        Returns:
            The details of the matrix.
        """
        endpoint = f'{self.base_matrices}/{matrix_id}'
        return self.auth.make_request('GET', endpoint)

class People:
    
    """
    A class representing a collection of companies.

    Attributes:
        auth (Auth): An instance of the Auth class used for authentication.

    Methods:
        list_consulted_people: Retrieves a list of consulted people.
        get_person_details: Retrieves the details of a specific person.
        is_person_approved: Returns status of last report of a person (approved or not)
        last_person_report: Returns the last report number of a person.
    """
    
    base_people = 'pessoas'

    def __init__(self, auth:IdwallAuth):
        self.auth = auth

    def list_consulted_people(self,size=25,page=1,**kwargs):
        """
        Retrieves a list of consulted people.
            
        Args:

            size (int): number of rows.
            
            page (int): number of pages.
            
        Returns:
            list: A list of consulted people.

        """
        payload = {'rows':size,'page':page}
        
        payload.update(kwargs)
        
        #
        return self.auth.make_request('GET', self.base_people,params=payload)

    def get_person_details(self, cpf:str, size=25,page=1, **kwargs):
        """
        Retrieves the details of a specific person.

        Args:
            cpf (str): The cpf of the person.
            
            size (int): number of rows.
            
            page (int): number of pages.

        Returns:
            dict: A dictionary containing the details of the person.

        """
        payload = {'rows':size,'page':page}
        payload.update(kwargs)
        
        endpoint = f'{self.base_people}/{cpf}'
        return self.auth.make_request('GET', endpoint, params=payload)
    
    def last_report_status(self, cpf: str):
        """
        Boolean with status of last report of a person (finished or not).

        Args:
            cpf (str): The cpf of the person.

        Returns:
            bool: True (approved) or False (rejected).

        """        
        person_details = self.get_person_details(cpf=cpf)
        status_last_report=person_details['result']['dados']['relatorios'][0]['status']
        if status_last_report == 'CONCLUIDO':
            return True
        else : return False
    
    def is_person_approved(self, cpf: str):
        """
        Boolean with status of last report of a person (approved or not).

        Args:
            cpf (str): The cpf of the person.

        Returns:
            bool: True (approved) or False (rejected).

        """        
        person_details = self.get_person_details(cpf=cpf)
        status_last_report=person_details['result']['dados']['relatorios'][0]['resultado']
        if status_last_report == 'VALID':
            return True
        else : return False
        
    def last_person_report(self, cpf: str):
        """
        Returns the last report number of a person.

        Args:
            cpf (str): The cpf of the person.

        Returns:
            str: String with the last report number of a person.

        """        
        person_details = self.get_person_details(cpf=cpf)
        return person_details['result']['dados']['relatorios'][0]['numero']
    
    #Criar metodo para puxar todo o historico de relatórios para uma pessoa json com lista de report numbers          
        
    def all_reports(self, cpf: str):
        """
        Returns all report numbers of a person.

        Args:
            cpf (str): The CPF of the person.

        Returns:
            list: List with all report numbers of a person.

        """
        person_details = self.get_person_details(cpf=cpf)
        
        # Check if person_details has the expected structure
        if 'result' in person_details and 'dados' in person_details['result']:
            pages = int(person_details['result']['paginacao']['total'])
            reports_list = person_details['result']['dados']['relatorios']
            
            if pages >= 2:
                for page in range(2, pages + 1):
                    relatorio = self.get_person_details(cpf=cpf, page=page)
                    # Assuming relatorio has the same structure as person_details
                    if 'result' in relatorio and 'dados' in relatorio['result']:
                        reports_list.extend(relatorio['result']['dados']['relatorios'])
            
            return reports_list
        else:
            # Handle the case where person_details does not have the expected structure
            return reports_list  # or raise an exception
        
class Companies:
    
    """
    A class representing a collection of people.

    Attributes:
        auth (Auth): An instance of the Auth class used for authentication.

    Methods:
        list_consulted_companies: Retrieves a list of consulted companies.
        get_company_details: Retrieves the details of a specific company.
        is_company_approved: Returns status of last report of a company (approved or not)
        last_company_report: Returns the last report number of a company.

    """
    
    base_companies = 'empresas'

    def __init__(self, auth:IdwallAuth):
        self.auth = auth

    def list_consulted_companies(self,size=25,page=1,**kwargs):
        """
        Retrieves a list of consulted people.
            
        Args:

            size (int): number of rows.
            
            page (int): number of pages.
            
        Returns:
            dict: A dict of consulted companies and some infos about them.

        """
        payload = {'rows':size,'page':page}
        
        payload.update(kwargs)
        
        #
        return self.auth.make_request('GET', self.base_companies,params=payload)

    def get_company_details(self, cnpj:str, size=25,page=1, **kwargs):
        """
        Retrieves the details of a specific person.

        Args:
            cnpj (str): The cnpj of the company.
            
            size (int): number of rows.
            
            page (int): number of pages.

        Returns:
            dict: A dictionary containing the details of the company.

        """
        payload = {'rows':size,'page':page}
        payload.update(kwargs)
        
        endpoint = f'{self.base_companies}/{cnpj}'
        return self.auth.make_request('GET', endpoint, params=payload)
    
    def is_company_approved(self, cnpj: str):
        """
        Boolean with status of last report of a person (approved or not).

        Args:
            cnpj (str): The cpf of the person.

        Returns:
            bool: True (approved) or False (rejected).

        """        
        company_details = self.get_company_details(cnpj=cnpj)
        status_last_report=company_details['result']['dados']['relatorios'][0]['resultado']
        if status_last_report == 'VALID':
            return True
        else : return False
        
    def last_company_report(self, cnpj: str):
        """
        Returns the last report number of a company.

        Args:
            cnpj (str): The cpf of the person.

        Returns:
            str: String with the last report number of a company.

        """        
        company_details = self.get_company_details(cnpj=cnpj)
        return company_details['result']['dados']['relatorios'][0]['numero']
    
    def all_reports(self, cnpj: str):
        """
        Returns all report numbers of a company.

        Args:
            cnpj (str): The CNPJ of the company.

        Returns:
            list: List with all report numbers of a person.

        """
        company_details = self.get_company_details(cnpj=cnpj)
        
        # Check if person_details has the expected structure
        if 'result' in company_details and 'dados' in company_details['result']:
            pages = int(company_details['result']['paginacao']['total'])
            reports_list = company_details['result']['dados']['relatorios']
            
            if pages >= 2:
                for page in range(2, pages + 1):
                    relatorio = self.get_company_details(cnpj=cnpj, page=page)
                    # Assuming relatorio has the same structure as person_details
                    if 'result' in relatorio and 'dados' in relatorio['result']:
                        reports_list.extend(relatorio['result']['dados']['relatorios'])
            
            return reports_list
        else:
            # Handle the case where person_details does not have the expected structure
            return reports_list  # or raise an exception
           
 

class Reports:
    base_reports = 'relatorios'
    """
    A class representing info about a specific report.

    Attributes:
        auth (Auth): An instance of the Auth class used for authentication.
        report_id (str): Code of the report

    Methods:
        get_report_status: Obtain the status of a specific report.
        manual_validation: Validate or invalidate a specific report.
        sent_parameters: Returns the sent parameters for an specific report creation.
        report_querys: Returns the most specific data from the queries that were performed.
        report_data: Returns the most specific data of a previously created report.
        report_validation_rules: Validation rules used to create a specific report.   
        report_finished: Returns if a report is finished or not.
        report_valid: Returns if a report is valid or not.
    """

    def __init__(self, auth:IdwallAuth, report_id):
        
        """
        Initializes an instance of Reports.

        Args:
            report (str): The number of a report.

        Attributes:
            auth (str): The authentication token.
            report_id (str): The number of a report.
            base_reports (str): The base URL for API requests.
        """
        self.auth = auth
        self.report_id=report_id
    
    def get_report_status(self):
        """
        Obtain the status of a specific report.
            
        Args:
            A report number.
            
        Returns:
            report_status(dict): Status of a report.

        """
                
        endpoint = f'{self.base_reports}/{self.report_id}'
        
        return self.auth.make_request('GET', endpoint)

    def manual_validation(self, aprovar:bool, mensagem:str, **kwargs):
        """
        Retrieves the details of a specific person.

        Args:
            aprovar (bolean): True (approval) or False (rejection).
            
            mensagem (str): reason for approval ou rejection (>=25 letters).

        Returns:
            dict: A dictionary containing infos about the operation or rejecting it (error).

        """
        payload = {'aprovar':aprovar,'mensagem':mensagem}
        payload.update(kwargs)
        
        endpoint = f'{self.base_reports}/validar/{self.report_id}'
        return self.auth.make_request('POST', endpoint, data=payload)
    
    def sent_parameters(self):
        """
        Returns the sent parameters for an specific report creation.

        Args:

        Returns:
            dict: A dictionary containing the sent parameters for a report that was previously created.

        """
        
        endpoint = f'{self.base_reports}/{self.report_id}/parametros'
        return self.auth.make_request('GET', endpoint)
    
    def report_querys(self):
        """
        Returns the most specific data from the queries that were performed.

        Args:

        Returns:
            dict: A dictionary containing the most specific data from queries that were performed for a report that was previously created.

        """
        
        endpoint = f'{self.base_reports}/{self.report_id}/consultas'
        return self.auth.make_request('GET', endpoint)
    
    def report_data(self)->dict:
        """
        Returns the most specific data from a created report.

        Args:

        Returns:
            dict: A dictionary containing the most specific data from a report that was previously created.

        """
        
        endpoint = f'{self.base_reports}/{self.report_id}/dados'
        return self.auth.make_request('GET', endpoint)
    
    def report_validation_rules(self):
        """
        Validation rules used to create a specific report.

        Args:

        Returns:
            dict: A dictionary containing validation rules used for a report that was previously created.

        """
        
        endpoint = f'{self.base_reports}/{self.report_id}/validacoes'
        return self.auth.make_request('GET', endpoint)
    
    def report_finished(self)->bool:
        """
        Boolean with status of a report finished (True) or not(False)   

        Args:

        Returns:
            bool: A boolen containing True (finished) or False (not finished).

        """        
        data = self.report_data()
        status = data.get('result',{}).get('status')
        
        if status =='CONCLUIDO': return True
        else: return False

    def report_valid(self)->bool:
        """
        Boolean with status of a report valid (True) or not(False)   

        Args:

        Returns:
            bool: A boolen containing True (valid) or False (not valid).

        """ 
        data = self.report_data()
        status = data.get('result',{}).get('resultado')
        
        if status == 'VALID':
            return True
        else : return False
        
class ReportManager():
    
    """
    A class to create reports or check general infos about reports of a specific token.

    Attributes:
        auth (Auth): An instance of the Auth class used for authentication.

    Methods:
        create_report: Creates an individual or legal entity report with the parameters previously sent.
        pending_reports: Returns reports that have not been completed so far.
        all_reports: Returns all reports that were created for a specific authentication token.
    """

    def __init__(self, auth:IdwallAuth):
        
        """
        Initializes an instance of Reports.

        Args:
            report (str): The number of a report.

        Attributes:
            auth (str): The authentication token.
            report_id (str): The number of a report.
            base_reports (str): The base URL for API requests.
        """
        self.auth = auth
        self.base_reports = 'relatorios'

    def create_report(self, matriz:str,document:Optional[str] = None,**kwargs):
        """
        Creates an individual or legal entity report with the parameters previously sent.

        Args:
            matriz (str): The matrix of the report which will be create
            cpf_data_nascimento (str): Date of birth in format 'DD/MM/YYYY' of the specific cpf used.
            cpf_nome (str): Name in the specific cpf used.
            cpf_numero (str): Cpf number.

        Returns:
            dict: A dictionary containing infos about the operation or rejecting it (error).

        """
        
        parametros = {}
        if len(document) ==14:#verifica se é um cnpj usando o tamanho do documento
            parametros.update({"cnpj_numero": document})
            
        else:
            parametros.update({"cpf_numero": document})
        
        parametros.update(**kwargs)
        
        payload = {
                    "matriz": matriz,
                    "parametros": parametros
                  }
        payload.update(kwargs)
        
        endpoint = f'{self.base_reports}'
        return self.auth.make_request('POST', endpoint, data=payload)
    
    def pending_reports(self):
        """
        Returns the unfinished reports until the moment.

        Args:

        Returns:
            dict: A dictionary containing the unfinished reports previously created.

        """
        
        endpoint = f'{self.base_reports}/pendentes'
        return self.auth.make_request('GET', endpoint)
    
    def all_reports(self):
        """
        Returns all reports that were created for a specific authentication token.

        Args:

        Returns:
            dict: A dictionary containing info about all reports that were created for a specific authentication token.

        """
        
        endpoint = f'{self.base_reports}'
        return self.auth.make_request('GET', endpoint)